"""install.sh とディスパッチャ ccskill-gptimage のテスト (issue #020)

HOME を一時ディレクトリに差し替えて実行するため、実環境の
~/.local/bin / ~/.claude/skills には触れない。
pip install は CCSKILL_GPTIMAGE_INSTALL_SKIP_DEPS=1 でスキップする
(venv はリポジトリに構築済みのものをディスパッチャが使う)。
"""

import os
import subprocess
from pathlib import Path

import pytest

REPO_DIR = Path(__file__).parent.parent
INSTALL_SH = REPO_DIR / "install.sh"
DISPATCHER = REPO_DIR / "ccskill-gptimage"


def _env(home: Path) -> dict:
    env = dict(os.environ)
    env["HOME"] = str(home)
    env["CCSKILL_GPTIMAGE_INSTALL_SKIP_DEPS"] = "1"
    return env


def _run_install(home: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["bash", str(INSTALL_SH), *args],
        capture_output=True,
        text=True,
        env=_env(home),
        cwd=REPO_DIR,
        timeout=120,
    )


def _run_dispatcher(home: Path, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    """インストール済み symlink 経由でディスパッチャを実行する"""
    link = home / ".local/bin/ccskill-gptimage"
    return subprocess.run(
        [str(link), *args],
        capture_output=True,
        text=True,
        env=_env(home),
        cwd=cwd or home,
        timeout=120,
    )


@pytest.fixture
def installed_home(tmp_path: Path) -> Path:
    """install.sh 実行済みの一時 HOME"""
    proc = _run_install(tmp_path)
    assert proc.returncode == 0, f"install.sh failed:\n{proc.stdout}\n{proc.stderr}"
    return tmp_path


class TestInstallScript:
    def test_install_exits_zero(self, tmp_path):
        proc = _run_install(tmp_path)
        assert proc.returncode == 0, f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"

    def test_creates_bin_symlink(self, installed_home):
        link = installed_home / ".local/bin/ccskill-gptimage"
        assert link.is_symlink()
        assert link.resolve() == DISPATCHER.resolve()

    def test_creates_user_skill_symlink(self, installed_home):
        link = installed_home / ".claude/skills/ccskill-gptimage"
        assert link.is_symlink()
        # symlink 経由で SKILL.md が解決できる(= Claude Code が認識できる)
        assert (link / "SKILL.md").is_file()
        assert link.resolve() == (REPO_DIR / ".claude/skills/ccskill-gptimage").resolve()

    def test_idempotent_rerun(self, installed_home):
        proc = _run_install(installed_home)
        assert proc.returncode == 0, f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        assert (installed_home / ".local/bin/ccskill-gptimage").is_symlink()
        assert (installed_home / ".claude/skills/ccskill-gptimage").is_symlink()

    def test_refuses_foreign_skill_dir(self, tmp_path):
        """SKILL.md を持たない実体ディレクトリが既にある場合は壊さずエラー"""
        foreign = tmp_path / ".claude/skills/ccskill-gptimage"
        foreign.mkdir(parents=True)
        (foreign / "keep.txt").write_text("do not delete")
        proc = _run_install(tmp_path)
        assert proc.returncode != 0
        assert (foreign / "keep.txt").exists()

    def test_replaces_stale_skill_copy(self, tmp_path):
        """SKILL.md を持つ実体ディレクトリ(過去の手動コピー)は symlink に置換する"""
        stale = tmp_path / ".claude/skills/ccskill-gptimage"
        stale.mkdir(parents=True)
        (stale / "SKILL.md").write_text("# old copy")
        proc = _run_install(tmp_path)
        assert proc.returncode == 0, f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        link = tmp_path / ".claude/skills/ccskill-gptimage"
        assert link.is_symlink()


class TestDispatcher:
    def test_version_exits_zero(self, installed_home):
        proc = _run_dispatcher(installed_home, "version")
        assert proc.returncode == 0
        assert "ccskill-gptimage" in proc.stdout

    def test_help_lists_subcommands(self, installed_home):
        proc = _run_dispatcher(installed_home, "help")
        assert proc.returncode == 0
        for sub in ("generate", "uninstall", "version", "help"):
            assert sub in proc.stdout

    def test_no_args_shows_help(self, installed_home):
        proc = _run_dispatcher(installed_home)
        assert proc.returncode == 0
        assert "generate" in proc.stdout

    def test_unknown_command_fails(self, installed_home):
        proc = _run_dispatcher(installed_home, "nosuchcommand")
        assert proc.returncode != 0

    def test_generate_wires_to_python_validation(self, installed_home, tmp_path):
        """別ディレクトリから generate がスクリプト本体まで届くこと。
        不正サイズは API 呼び出し前に exit 2 + 日本語エラーで返る(課金なし)"""
        workdir = tmp_path / "elsewhere"
        workdir.mkdir(parents=True, exist_ok=True)
        proc = _run_dispatcher(
            installed_home, "generate", "test prompt", "--size", "1000x1000",
            cwd=workdir,
        )
        assert proc.returncode == 2
        assert "16" in proc.stdout

    def test_generate_help_passthrough(self, installed_home):
        proc = _run_dispatcher(installed_home, "generate", "--help")
        assert proc.returncode == 0
        assert "--size" in proc.stdout


class TestUninstall:
    def test_uninstall_removes_symlinks(self, installed_home):
        proc = _run_dispatcher(installed_home, "uninstall")
        assert proc.returncode == 0
        assert not (installed_home / ".local/bin/ccskill-gptimage").exists()
        assert not (installed_home / ".claude/skills/ccskill-gptimage").exists()

    def test_uninstall_keeps_repo_intact(self, installed_home):
        _run_dispatcher(installed_home, "uninstall")
        assert DISPATCHER.exists()
        assert (REPO_DIR / ".claude/skills/ccskill-gptimage/SKILL.md").exists()
