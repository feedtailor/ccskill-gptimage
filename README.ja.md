# ccskill-gptimage 画像生成スキル

[English README](README.md)

OpenAI **gpt-image-2** (ChatGPT Images 2.0) を使用した Claude Code 用画像生成スキルです。画像生成スクリプト単体としても使用できます。
(Nano Banana Pro を使ったスキルはこちら → [feedtailor/ccskill-nanobanana](https://github.com/feedtailor/ccskill-nanobanana))

## 特徴

プロンプトを明示的に指定する必要がなく、プロジェクト内の情報やコンテキストを踏まえた最適なプロンプトを自動生成して、Claude Code のセッション内で画像生成を行います。

画像生成AIとして ChatGPT Image 2.0 を使用することで、以下のような特徴を備えた画像生成ワークフローを組むことができます。

- **多言語テキスト描画** — 日本語(漢字/かな)・絵文字混在のポスターやバナーが一発で読める品質
- **Agentic 推論** — 業界初のエージェント型画像生成モデル。プロンプトから構造を計画して描画
- **参照画像で編集** — `--reference` で既存画像をベースに合成・部分修正
- **マスク編集 (inpainting)** — 既存画像の部分置換
- **メタデータ自動保存** — プロンプト・revised_prompt・パラメータを JSON サイドカーに記録
- **コスト最適化済みデフォルト** — 縦長 high が正方形 high より安い等の非自明な知見を組み込み

## 作例

本スキルを使って生成した画像の作例。プロンプトはスキルによる自動生成。全作例は [`docs/gallery.md`](docs/gallery.md) を参照。

<table>
<tr>
  <td align="center" width="33%"><img src="assets/capability-survey/categories/v2/01_photorealistic_portrait_woman.png" width="260" alt="写実ポートレート"></td>
  <td align="center" width="33%"><img src="assets/capability-survey/categories/v2/19_urban_tokyo_rainy_night_v3.png" width="260" alt="渋谷スクランブル交差点・雨上がりの夜"></td>
  <td align="center" width="33%"><a href="docs/gallery.md"><img src="assets/capability-survey/categories/v2/18_nature_volcanic_coast_dawn.png" width="260" alt="フルギャラリーを見る"></a></td>
</tr>
<tr>
  <td align="center" width="33%"><img src="assets/capability-survey/categories/v2/24_line_drawing_fashion_sketch.png" width="260" alt="線画(ファッションスケッチ)"></td>
  <td align="center" width="33%"><img src="assets/capability-survey/categories/v2/14_japanese_poster_vertical_tategaki.png" width="260" alt="日本語縦書きポスター"></td>
  <td align="center" width="33%"><img src="assets/capability-survey/categories/v2/06_ui_mockup_settings_japanese.png" width="260" alt="日本語 iOS 設定 UI"></td>
</tr>
</table>

## セットアップ

### 必要環境(2 つの利用パターン)

本スキルは 2 つの backend のどちらかが利用可能なら動きます:

**パターン A: ChatGPT サブスク + Codex CLI(推奨・API キー不要)**
- **Python 3.10 以上**
- **ChatGPT サブスク契約**(Plus 以上)
- **[Codex CLI](https://github.com/openai/codex) インストール済み + `codex login` でログイン済み**
- → API キー不要、追加課金なし(サブスク枠内で使える)

**パターン B: OpenAI API キー(従来通り)**
- **Python 3.10 以上**
- **OpenAI API キー** + **Organization Verification 済み**(未検証 Org では 403)
- → 1 枚あたり数セント〜数十セントの従量課金

両方ある環境なら `--backend auto`(デフォルト)が Codex を優先 → 失敗時は API へ自動フォールバック。

### 1. リポジトリのクローン

```bash
cd /path/to/your-projects
git clone https://github.com/feedtailor/ccskill-gptimage.git
cd ccskill-gptimage
```

### 2. backend の準備

**パターン A を使う場合**(Codex CLI):

```bash
# Codex CLI をインストール(Homebrew)
brew install codex
# ChatGPT アカウントでログイン
codex login
# 確認: tokens.access_token が入っていれば OK
cat ~/.codex/auth.json | python -c "import sys,json;print('OK' if json.load(sys.stdin).get('tokens',{}).get('access_token') else 'NG')"
```

**パターン B を使う場合**(API キー):

1. [OpenAI Platform](https://platform.openai.com/api-keys) にアクセスして API キーを発行
2. **Organization が Verified 状態になっていること**(Settings → General → Verifications)を確認
3. 課金設定が必要(`gpt-image-2` は無料枠なし)

### 3. 環境変数の設定(API キーを使う場合のみ)

```bash
cp .env.example .env
```

`.env` を編集:
```
OPENAI_API_KEY=sk-...
```

### 4. 依存パッケージのインストール

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

### 5. 環境変数の設定 (スキルとして使用する場合)

`.bashrc` / `.zshrc` に追加:
```bash
export CCSKILL_GPTIMAGE_DIR="/path/to/ccskill-gptimage"
```

## 使い方

### コマンドラインから直接実行

```bash
source venv/bin/activate
python generate_image.py "夕焼けの海岸線"
```

### オプション

| オプション | 説明 | デフォルト |
|---|---|---|
| `--size` | 出力サイズ (`auto`/`1024x1024`/`1024x1536`/`1536x1024`) | `1024x1024` |
| `--quality` | 品質 (`auto`/`low`/`medium`/`high`) | `auto` |
| `--background` | 背景 (`auto`/`opaque`)。`transparent` は gpt-image-2 未対応(`gpt-image-1.5` で対応) | `auto` |
| `--output-format` | 出力形式 (`png`/`jpeg`/`webp`) | `png` |
| `--output-compression` | 圧縮率 (jpeg/webp 時 0-100) | なし |
| `--output` | 出力ディレクトリ | `./generated_images` |
| `--reference` | 参照画像 (複数指定可) | なし |
| `--mask` | マスク画像 (透明部分が編集対象) | なし |
| `--input-fidelity` | gpt-image-2 では指定不要(常に最大忠実度)。`gpt-image-1.5` 用 | なし |
| `--moderation` | モデレーション (`auto`/`low`) | `auto` |
| `--backend` | 画像生成 backend (`auto`/`codex`/`api`)。`auto` は Codex 優先、失敗時 API フォールバック | `auto` |

### 使用例

```bash
# 基本
python generate_image.py "A minimalist fox logo, flat vector, navy and gold"

# 日本語ポスター
python generate_image.py 'A minimalist editorial poster with the exact title "腹落ちDMARC" in large serif Japanese font, dark navy background' --size 1024x1536 --quality high

# 参照画像をベースに編集(背景置換)
python generate_image.py "Place the same fox logo on a deep navy background with subtle gold sparkles. Preserve the fox's pose and proportions from the reference." --reference ./logo.png --quality medium

# 複数参照を合成
python generate_image.py "Photorealistic gift basket on white" --reference ./a.png --reference ./b.png --reference ./c.png

# マスク編集 (inpainting)
python generate_image.py "A sunlit indoor lounge with a pool" --reference ./lounge.png --mask ./mask.png
```

### 出力ファイル

各画像と並列に **メタデータ JSON サイドカー** (`{画像名}.{ext}.json`) が保存され、再現/微調整に使えます:
```json
{
  "model": "gpt-image-2",
  "prompt": "...",
  "revised_prompt": "...",
  "size": "1024x1024",
  "quality": "high",
  "timestamp": "2026-04-23T10:00:00"
}
```

## Claude Code スキルとして使用

### 他のプロジェクトへのインストール

シンボリックリンクで配置:

```bash
mkdir -p /path/to/your-project/.claude/skills

ln -s $CCSKILL_GPTIMAGE_DIR/.claude/skills/ccskill-gptimage \
      /path/to/your-project/.claude/skills/ccskill-gptimage
```

これで Claude Code から画像生成が必要な場面でこのスキルが自動利用されます。リポジトリを `git pull` すれば、リンク先プロジェクトの参照スキルも自動更新されます。

### スキル言語の設定

デフォルトでは英語版 (`SKILL.md`) が使用されます。日本語版に切り替える場合:

```bash
cd $CCSKILL_GPTIMAGE_DIR/.claude/skills/ccskill-gptimage

mv SKILL.md SKILL.en.md
ln -s SKILL.ja.md SKILL.md
```

## テスト

```bash
source venv/bin/activate
python -m pytest tests/ -v
```

API 呼び出しは全てモックされているため、テスト実行に API キーは不要です。

## 仕様

- **モデル**: `gpt-image-2`(`gpt-image-2-2026-04-21` スナップショット)
- **入力**: テキスト / 画像
- **出力**: 画像のみ(`b64_json` 形式、URLは返らない)
- **最大解像度**: 2K
- **エンドポイント**: `/v1/images/generations`, `/v1/images/edits`
- **ファイル名**: タイムスタンプ形式 (例: `20260423_153045.png`)
- **モデレーション**: `auto`(デフォルト) / `low`

## 姉妹スキル `ccskill-nanobanana` との使い分け

| 用途 | 第一選択 | 理由 |
|---|---|---|
| 日本語/漢字テキスト入りビジュアル | **ccskill-gptimage** | gpt-image-2 のテキスト描画が最強 |
| ビジネスインフォグラフィック | **ccskill-gptimage** | Agentic 推論で構造を計画 |
| 既存画像の編集・部分修正 | **ccskill-gptimage** | 入力画像を常に最大忠実度で処理 |
| 透過 PNG (ロゴ・アイコン・スプライト) | どちらでも | gpt-image-2 は不可だが `--model gpt-image-1.5` で対応可。後処理 (rembg) も現実的 |
| 4K 出力 | **ccskill-nanobanana** | gpt-image-2 は 2K まで |

## トラブルシューティング

| 症状 | 対処 |
|---|---|
| `403 Forbidden` | OpenAI Organization Verification が未完了 → Settings で完了させる |
| `Rate limit exceeded` | Tier 1 は 5 IPM のみ。本番運用は Tier 3+ 推奨 |
| タイムアウト | SDK のタイムアウトを 120 秒以上に設定 |
| 日本語が崩れる | プロンプト内のテキストを `" "` で正確に囲み、フォント指定 (`serif Japanese font` 等) を明示 |

## ライセンス

MIT
