"""ccskill-gptimage doctor サブコマンドのテスト (issue #021)

設計原則(#021):
  - doctor は秘密ファイルの中身を一切読まない(env 変数の有無 + ファイル存在のみ)
  - 出力に API キー / access_token の値が現れてはならない
  - backend が 1 つも presence 無し → exit 1、最低 1 つあれば exit 0
  - Org Verification はライブ判定せず静的案内のみ

HOME を一時ディレクトリに隔離して実環境に触れない。backend 無しの負経路は
「fake repo(dispatcher + venv symlink のみ、.env 無し)」+ codex を除いた PATH で再現する。
"""

import os
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_DIR = Path(__file__).parent.parent
DISPATCHER = REPO_DIR / "ccskill-gptimage"
INSTALL_SH = REPO_DIR / "install.sh"
REAL_VENV = REPO_DIR / "venv"

# codex を含まない最小 PATH(coreutils は要る)。doctor の Codex presence を確実に false にする。
MINIMAL_PATH = "/usr/bin:/bin:/usr/sbin:/sbin"


def _base_env(home: Path) -> dict:
    env = dict(os.environ)
    env["HOME"] = str(home)
    return env


def _run_doctor(env: dict, cwd: Path | None = None, dispatcher: Path = DISPATCHER):
    return subprocess.run(
        [str(dispatcher), "doctor"],
        capture_output=True,
        text=True,
        env=env,
        cwd=cwd or REPO_DIR,
        timeout=60,
    )


@pytest.fixture
def installed_home(tmp_path: Path) -> Path:
    """install.sh 実行済みの一時 HOME(symlink が ✓ になる)"""
    env = _base_env(tmp_path)
    env["CCSKILL_GPTIMAGE_INSTALL_SKIP_DEPS"] = "1"
    proc = subprocess.run(
        ["bash", str(INSTALL_SH)],
        capture_output=True, text=True, env=env, cwd=REPO_DIR, timeout=120,
    )
    assert proc.returncode == 0, f"install.sh failed:\n{proc.stdout}\n{proc.stderr}"
    return tmp_path


def _make_fake_repo(tmp_path: Path) -> Path:
    """dispatcher と venv symlink だけを持つ偽 repo(.env 無し)。
    API backend を presence 無しにするために使う。"""
    fake = tmp_path / "fake_repo"
    fake.mkdir()
    shutil.copy2(DISPATCHER, fake / "ccskill-gptimage")
    (fake / "ccskill-gptimage").chmod(0o755)
    (fake / "venv").symlink_to(REAL_VENV)
    return fake


class TestDoctorBasic:
    def test_doctor_runs_in_repo(self, tmp_path):
        """本 repo(.env あり)では backend presence ありで exit 0"""
        proc = _run_doctor(_base_env(tmp_path))
        assert proc.returncode == 0, f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"

    def test_doctor_lists_all_sections(self, tmp_path):
        proc = _run_doctor(_base_env(tmp_path))
        out = proc.stdout
        # 主要セクションの語が含まれること
        assert "Python" in out
        assert "Codex" in out
        assert "API" in out
        assert "Verification" in out

    def test_doctor_help_lists_doctor(self, tmp_path):
        proc = subprocess.run(
            [str(DISPATCHER), "help"],
            capture_output=True, text=True, env=_base_env(tmp_path), timeout=30,
        )
        assert proc.returncode == 0
        assert "doctor" in proc.stdout


class TestDoctorSecretHygiene:
    def test_doctor_never_prints_api_key(self, tmp_path):
        """出力に OpenAI キーらしき文字列が現れない(秘密非漏洩)"""
        proc = _run_doctor(_base_env(tmp_path))
        combined = proc.stdout + proc.stderr
        assert "sk-" not in combined
        assert "access_token" not in combined

    def test_doctor_does_not_echo_injected_key(self, tmp_path):
        """env に注入したダミーキー値が出力に漏れない"""
        env = _base_env(tmp_path)
        env["OPENAI_API_KEY"] = "sk-doctortest-SHOULD-NOT-LEAK-1234567890"
        proc = _run_doctor(env)
        combined = proc.stdout + proc.stderr
        assert "SHOULD-NOT-LEAK" not in combined
        assert "sk-doctortest" not in combined


class TestDoctorBackendDetection:
    def test_api_presence_via_env_var(self, tmp_path):
        """OPENAI_API_KEY があれば API backend は presence あり扱い"""
        env = _base_env(tmp_path)
        env["OPENAI_API_KEY"] = "sk-dummy-value-not-printed"
        proc = _run_doctor(env)
        assert proc.returncode == 0
        # 値は出さず presence だけ
        assert "API" in proc.stdout

    def test_no_backend_exits_one(self, tmp_path):
        """fake repo(.env 無し)+ codex 無し PATH + key 無し → backend 総合 ✗ → exit 1"""
        fake = _make_fake_repo(tmp_path)
        env = _base_env(tmp_path)
        env.pop("OPENAI_API_KEY", None)
        env["PATH"] = MINIMAL_PATH
        proc = _run_doctor(env, dispatcher=fake / "ccskill-gptimage")
        assert proc.returncode == 1, f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"

    def test_no_backend_still_no_secret(self, tmp_path):
        fake = _make_fake_repo(tmp_path)
        env = _base_env(tmp_path)
        env.pop("OPENAI_API_KEY", None)
        env["PATH"] = MINIMAL_PATH
        proc = _run_doctor(env, dispatcher=fake / "ccskill-gptimage")
        assert "sk-" not in (proc.stdout + proc.stderr)


class TestDoctorWithFullInstall:
    def test_symlinks_reported_ok_after_install(self, installed_home):
        """install 済み HOME では PATH コマンド / user skill が ✓ で exit 0"""
        env = _base_env(installed_home)
        # repo の .env があるため backend は presence あり
        proc = _run_doctor(env)
        assert proc.returncode == 0
        out = proc.stdout
        # symlink 解決が成功している旨(✓ マーク or 明示語)
        assert "skills" in out or "skill" in out.lower()
