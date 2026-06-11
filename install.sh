#!/bin/bash
#
# ccskill-gptimage - Installer (issue #020)
#
# clone → cd → ./install.sh だけで、どのプロジェクトからでも
# 人間にも AI (Claude Code) にも使える状態にする。
#
#   1. python3 (>= 3.10) チェック
#   2. venv 構築 + 依存インストール(冪等)
#   3. ~/.local/bin/ccskill-gptimage symlink 配備(PATH コマンド化)
#   4. ~/.claude/skills/ccskill-gptimage symlink 登録(ユーザレベルスキル)
#   5. backend(Codex CLI / OPENAI_API_KEY)利用可否の診断表示
#
# Usage: ./install.sh
#
# 環境変数:
#   CCSKILL_GPTIMAGE_INSTALL_SKIP_DEPS=1  pip install をスキップ(テスト用)
#

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 自身の位置から repo ディレクトリを解決(symlink 経由でも辿る)
SCRIPT_PATH="$0"
while [ -L "$SCRIPT_PATH" ]; do
    LINK_TARGET=$(readlink "$SCRIPT_PATH")
    case "$LINK_TARGET" in
        /*) SCRIPT_PATH="$LINK_TARGET" ;;
        *)  SCRIPT_PATH="$(dirname "$SCRIPT_PATH")/$LINK_TARGET" ;;
    esac
done
REPO_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"

echo "================================================"
echo "  ccskill-gptimage - Installer"
echo "================================================"
echo ""
echo "Master: $REPO_DIR"
echo ""

# ========================================
# 1. python3 チェック (>= 3.10)
# ========================================

echo "Step 1: Checking prerequisites..."

# 3.10+ の Python を探索(macOS のシステム python3 は 3.9 のため、
# バージョン付きコマンドを優先して探す)
_py_ok() {
    "$1" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null
}

VENV_PYTHON="$REPO_DIR/venv/bin/python"

PYTHON_BIN=""
if [ -x "$VENV_PYTHON" ] && _py_ok "$VENV_PYTHON"; then
    # 既存 venv が有効ならそれを使う(システム Python は不問)
    PYTHON_BIN="$VENV_PYTHON"
else
    for cand in python3.13 python3.12 python3.11 python3.10 python3; do
        if command -v "$cand" &> /dev/null && _py_ok "$cand"; then
            PYTHON_BIN="$cand"
            break
        fi
    done
fi

if [ -z "$PYTHON_BIN" ]; then
    echo -e "${RED}Error: Python 3.10+ is required but was not found${NC}"
    echo "Install it first (e.g. brew install python@3.13): https://www.python.org/"
    exit 1
fi

echo -e "${GREEN}✓ Python found: $PYTHON_BIN ($("$PYTHON_BIN" -c 'import sys; print(".".join(map(str, sys.version_info[:3])))'))${NC}"
echo ""

# ========================================
# 2. venv 構築 + 依存インストール(冪等)
# ========================================

echo "Step 2: Setting up Python environment..."

if [ ! -x "$VENV_PYTHON" ]; then
    "$PYTHON_BIN" -m venv "$REPO_DIR/venv"
    echo -e "${GREEN}✓ venv created${NC}"
else
    echo -e "${GREEN}✓ venv already exists${NC}"
fi

if [ "${CCSKILL_GPTIMAGE_INSTALL_SKIP_DEPS:-}" = "1" ]; then
    echo -e "${YELLOW}(dependencies skipped: CCSKILL_GPTIMAGE_INSTALL_SKIP_DEPS=1)${NC}"
else
    "$VENV_PYTHON" -m pip install --quiet --disable-pip-version-check -r "$REPO_DIR/requirements.txt"
    echo -e "${GREEN}✓ Dependencies installed${NC}"
fi
echo ""

# ========================================
# 3. ~/.local/bin への symlink 配備
# ========================================

echo "Step 3: Installing 'ccskill-gptimage' command..."

BIN_DIR="$HOME/.local/bin"
BIN_LINK="$BIN_DIR/ccskill-gptimage"
DISPATCHER="$REPO_DIR/ccskill-gptimage"

mkdir -p "$BIN_DIR"

if [ -L "$BIN_LINK" ] || [ ! -e "$BIN_LINK" ]; then
    ln -sf "$DISPATCHER" "$BIN_LINK"
    echo -e "${GREEN}✓ Command installed: $BIN_LINK${NC}"
else
    echo -e "${RED}Error: $BIN_LINK exists and is not a symlink${NC}"
    echo "Remove it manually and re-run ./install.sh"
    exit 1
fi

# PATH チェック
if echo "$PATH" | tr ':' '\n' | grep -qx "$BIN_DIR"; then
    echo -e "${GREEN}✓ $BIN_DIR is in PATH${NC}"
else
    echo ""
    echo -e "${YELLOW}$BIN_DIR is not in your PATH.${NC}"
    SHELL_NAME=$(basename "${SHELL:-sh}")
    case "$SHELL_NAME" in
        zsh)  RC_FILE="~/.zshrc" ;;
        bash) RC_FILE="~/.bashrc" ;;
        *)    RC_FILE="your shell config" ;;
    esac
    echo "Add this to $RC_FILE and reload your shell:"
    echo ""
    echo -e "  ${BLUE}export PATH=\"\$HOME/.local/bin:\$PATH\"${NC}"
fi
echo ""

# ========================================
# 4. ユーザレベルスキル登録 (~/.claude/skills)
# ========================================

echo "Step 4: Registering user-level skill for Claude Code..."

SKILL_SRC="$REPO_DIR/.claude/skills/ccskill-gptimage"
SKILL_PARENT="$HOME/.claude/skills"
SKILL_LINK="$SKILL_PARENT/ccskill-gptimage"

if [ ! -f "$SKILL_SRC/SKILL.md" ]; then
    echo -e "${RED}Error: skill source not found: $SKILL_SRC${NC}"
    exit 1
fi

mkdir -p "$SKILL_PARENT"

if [ -L "$SKILL_LINK" ]; then
    /bin/rm -f "$SKILL_LINK"
elif [ -d "$SKILL_LINK" ]; then
    if [ -f "$SKILL_LINK/SKILL.md" ]; then
        # 過去の手動コピーとみなして symlink に置換
        /bin/rm -rf "$SKILL_LINK"
    else
        echo -e "${RED}Error: $SKILL_LINK exists but does not look like ccskill-gptimage (no SKILL.md).${NC}"
        echo "Remove it manually and re-run ./install.sh"
        exit 1
    fi
elif [ -e "$SKILL_LINK" ]; then
    echo -e "${RED}Error: $SKILL_LINK exists and is not a directory/symlink.${NC}"
    echo "Remove it manually and re-run ./install.sh"
    exit 1
fi

ln -s "$SKILL_SRC" "$SKILL_LINK"

if [ ! -f "$SKILL_LINK/SKILL.md" ]; then
    /bin/rm -f "$SKILL_LINK"
    echo -e "${RED}Error: symlink could not be resolved on this filesystem.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ User skill registered: $SKILL_LINK${NC}"
echo "  -> $SKILL_SRC"
echo "  (available in every Claude Code project; auto-updates via git pull)"
echo ""

# ========================================
# 5. backend 利用可否の診断(presence ベース。秘密ファイルの中身は読まない: issue #021)
# ========================================

echo "Step 5: Checking image-generation backends (presence-based; secrets not read)..."

# Codex: CLI の存在 + ログインセッションファイルの存在のみで判定(token は読まない)
CODEX_OK=false
if command -v codex &> /dev/null && [ -f "$HOME/.codex/auth.json" ]; then
    CODEX_OK=true
fi

# API: 環境変数の有無 + .env ファイルの存在のみで判定(.env の中身は読まない)
API_OK=false
if [ -n "${OPENAI_API_KEY:-}" ]; then
    API_OK=true
elif [ -f "$REPO_DIR/.env" ]; then
    API_OK=true
fi

if [ "$CODEX_OK" = true ]; then
    echo -e "${GREEN}✓ Codex CLI backend: likely (codex CLI + login session present)${NC}"
else
    echo -e "${YELLOW}- Codex CLI backend not available${NC} (brew install codex && codex login)"
fi

if [ "$API_OK" = true ]; then
    echo -e "${GREEN}✓ OpenAI API backend: likely (OPENAI_API_KEY set or .env present)${NC}"
else
    echo -e "${YELLOW}- OpenAI API backend not configured${NC} (cp .env.example .env, then set OPENAI_API_KEY)"
fi

if [ "$CODEX_OK" != true ] && [ "$API_OK" != true ]; then
    echo ""
    echo -e "${YELLOW}Warning: No backend is available yet.${NC}"
    echo "Set up at least one backend before generating images — see README.md (Requirements)."
fi
echo ""

# ========================================
# 完了
# ========================================

echo "================================================"
echo -e "${GREEN}  Installation Complete!${NC}"
echo "================================================"
echo ""
echo "Try it from any directory:"
echo ""
echo -e "  ${BLUE}ccskill-gptimage generate \"a minimalist fox logo, flat vector\"${NC}"
echo ""
echo "Or in any Claude Code project, just ask:"
echo ""
echo "  \"Generate an image of ... with ChatGPT Images\""
echo ""
echo "To update later:  cd $REPO_DIR && git pull"
echo "To uninstall:     ccskill-gptimage uninstall"
echo ""
