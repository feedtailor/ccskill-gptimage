#!/usr/bin/env python3
"""Phase 4 比較 (issue #017): 35 枚を Codex CLI backend 経由で再生成して v2 (API) と比較する。

- 出力先: assets/capability-survey/categories/v3-codex/ + grid/v3-codex/
- 既存ファイルがあればスキップ(再開可能)
- レート上限/クォータ超過と思しきエラーを検出したら即終了し、何枚で何秒で詰まったかを記録
"""
from __future__ import annotations

import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
PY = ROOT / "venv" / "bin" / "python"
GEN = ROOT / "generate_image.py"
OUT_CAT = ROOT / "assets" / "capability-survey" / "categories" / "v3-codex"
OUT_GRID = ROOT / "assets" / "capability-survey" / "grid" / "v3-codex"
LOG = ROOT / "docs" / "_tmp_codex_regen.log"

OUT_CAT.mkdir(parents=True, exist_ok=True)
OUT_GRID.mkdir(parents=True, exist_ok=True)
LOG.parent.mkdir(parents=True, exist_ok=True)

# レート上限・クォータ枯渇と思われるパターン(case-insensitive)
QUOTA_PATTERNS = [
    r"rate[\s\-_]?limit",
    r"quota",
    r"too many requests",
    r"\b429\b",
    r"insufficient[\s_]quota",
    r"usage[\s_]limit",
    r"exceed(ed|s)?",
    r"throttled",
    r"plan\s+limit",
    r"daily\s+limit",
    r"monthly\s+limit",
]
QUOTA_RE = re.compile("|".join(QUOTA_PATTERNS), re.IGNORECASE)

# (name, size, quality, prompt) — phase4 と同一プロンプト
CATEGORIES: list[tuple[str, str, str, str]] = []
GRID_PROMPT_V2 = ""
GRID_CELLS: list[tuple[str, str, str]] = []


def _load_prompts() -> None:
    """phase4 のプロンプト定義を git から取得して in-memory にロード"""
    global CATEGORIES, GRID_PROMPT_V2, GRID_CELLS
    res = subprocess.run(
        ["git", "-C", str(ROOT), "show", "10dccdc:scripts/phase4_regenerate.py"],
        capture_output=True, text=True, check=True,
    )
    src = res.stdout
    # ROOT 等の path 依存を切るため、module としては実行せず、定義部分だけ exec する
    # 簡易: 直接 exec するが、危険な副作用は無いと git で確認済み
    namespace: dict = {
        "__name__": "phase4_loaded",
        "__file__": str(ROOT / "scripts" / "_phase4_loader_stub.py"),
    }
    exec(src, namespace)
    CATEGORIES = namespace["CATEGORIES"]
    GRID_PROMPT_V2 = namespace["GRID_PROMPT_V2"]
    GRID_CELLS = namespace["GRID_CELLS"]


def _is_quota_error(text: str) -> bool:
    if not text:
        return False
    return bool(QUOTA_RE.search(text))


def run_one(
    prompt: str, size: str, quality: str, output_dir: Path, output_name: str
) -> tuple[str, float, str]:
    """1 枚生成。戻り値: (status, elapsed_sec, message)
    status は "ok" / "skip" / "fail" / "quota" のいずれか。"""
    existing = output_dir / f"{output_name}.png"
    if existing.exists() and existing.stat().st_size > 0:
        return ("skip", 0.0, "already exists")

    cmd = [
        str(PY), str(GEN), prompt,
        "--backend", "codex",
        "--size", size,
        "--quality", quality,
        "--output", str(output_dir),
        "--output-name", output_name,
    ]
    t0 = time.time()
    res = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time() - t0
    combined = (res.stdout or "") + "\n" + (res.stderr or "")

    if _is_quota_error(combined):
        return ("quota", elapsed, combined.strip()[:500])
    if res.returncode != 0 or not existing.exists():
        return ("fail", elapsed, (res.stderr.strip() or res.stdout.strip())[:500])
    return ("ok", elapsed, "")


def main(argv: list[str]) -> int:
    _load_prompts()

    prefix = argv[1] if len(argv) > 1 else None

    tasks: list[tuple[str, str, str, str, Path]] = []
    for name, size, quality, prompt in CATEGORIES:
        if prefix and not name.startswith(prefix):
            continue
        tasks.append((name, size, quality, prompt, OUT_CAT))
    for name, size, quality in GRID_CELLS:
        if prefix and not name.startswith(prefix):
            continue
        tasks.append((name, size, quality, GRID_PROMPT_V2, OUT_GRID))

    total = len(tasks)
    counts = {"ok": 0, "skip": 0, "fail": 0, "quota": 0}
    timings: list[float] = []
    start = time.time()
    log_lines: list[str] = []

    def emit(line: str) -> None:
        print(line, flush=True)
        log_lines.append(line)

    emit(f"=== Codex regenerate start: {total} tasks (issue #017 gate 2) ===")
    for i, (name, size, quality, prompt, outdir) in enumerate(tasks, 1):
        status, elapsed, msg = run_one(prompt, size, quality, outdir, name)
        elapsed_total = time.time() - start
        counts[status] += 1
        if status == "ok":
            timings.append(elapsed)
        line = (
            f"[{i:02d}/{total}] {name}  size={size}  quality={quality}  "
            f"status={status}  elapsed={elapsed:.0f}s  total={elapsed_total:.0f}s"
        )
        if msg and status != "ok":
            line += f"  msg={msg[:200]}"
        emit(line)
        if status == "quota":
            emit("")
            emit("=== QUOTA / RATE-LIMIT detected — abort immediately ===")
            emit(f"  reached: {i - 1}/{total} successful before failure")
            emit(f"  elapsed: {elapsed_total:.0f}s")
            emit(f"  per-image avg: {(sum(timings) / len(timings)):.0f}s" if timings else "  per-image avg: n/a")
            emit("  detected pattern in last response (truncated):")
            emit(f"  {msg[:500]}")
            LOG.write_text("\n".join(log_lines) + "\n")
            return 2

    elapsed_total = time.time() - start
    emit("")
    emit("=== Codex regenerate complete ===")
    emit(f"  ok: {counts['ok']}  skip: {counts['skip']}  fail: {counts['fail']}  quota: {counts['quota']}")
    emit(f"  elapsed: {elapsed_total:.0f}s  ({elapsed_total/60:.1f} min)")
    if timings:
        emit(f"  per-image avg: {sum(timings)/len(timings):.0f}s  min: {min(timings):.0f}s  max: {max(timings):.0f}s")
    LOG.write_text("\n".join(log_lines) + "\n")
    return 0 if counts["fail"] == 0 and counts["quota"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
