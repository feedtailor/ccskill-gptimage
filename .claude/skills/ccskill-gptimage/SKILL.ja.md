---
name: ccskill-gptimage
description: |
  画像生成が必要な時に使用するスキル。
  OpenAI gpt-image-2 (ChatGPT Images 2.0) で高品質な画像を生成・編集します。
  日本語/多言語テキスト描画、Agentic 推論、参照画像保持、透過 PNG、複雑インフォグラフィックに強い。
---

# ccskill-gptimage 画像生成スキル

## 概要

このスキルは OpenAI gpt-image-2 を使って画像を生成・編集します。**ユーザは「こんな画像が欲しい」と意図を伝えるだけで十分** で、プロンプトの構造化・スタイル指定・コスト最適化は Claude が会話履歴とプロジェクト文脈から自動で組み立てます。姉妹スキル `ccskill-nanobanana` (Gemini 3 Pro Image) と用途で使い分けます。

## 前提条件

- 環境変数 `CCSKILL_GPTIMAGE_DIR` にこのスキルのリポジトリパスを設定
  ```bash
  export CCSKILL_GPTIMAGE_DIR="$HOME/projects/ccskill-gptimage"
  ```
- 環境変数 `OPENAI_API_KEY` が設定されていること(または `$CCSKILL_GPTIMAGE_DIR/.env` に記載)
- **OpenAI Organization Verification 済みであること**(未検証 Org では 403 になる)

## 使い方

```bash
$CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py "プロンプト"
```

### オプション

| オプション | 説明 | デフォルト | 値 |
|---|---|---|---|
| `--size` | 出力サイズ | `1024x1024` | `auto` / `1024x1024` / `1024x1536` (縦長) / `1536x1024` (横長) |
| `--quality` | 品質 | `auto` | `auto` / `low` / `medium` / `high` |
| `--background` | 背景 | `auto` | `auto` / `opaque` (`transparent` は gpt-image-2 非対応 — `--model gpt-image-1.5` で対応可) |
| `--output-format` | 出力形式 | `png` | `png` / `jpeg` / `webp` |
| `--output-compression` | 圧縮率(jpeg/webp) | なし | 0-100 |
| `--output` | 出力ディレクトリ | `./generated_images` | 任意のパス |
| `--reference` | 参照画像(複数指定可) | なし | 画像ファイルパス |
| `--mask` | マスク画像(透明部分が編集対象、`--reference` 必須) | なし | 画像ファイルパス |
| `--input-fidelity` | gpt-image-2 では指定不要(常に最大忠実度)。`--model gpt-image-1.5` 用 | なし | `high` / `low` |
| `--moderation` | モデレーション | `auto` | `auto` / `low` |
| `--model` | モデル ID | `gpt-image-2` | 任意のモデル ID |

### 使用例

#### 基本

```bash
$CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py \
  "A children's book illustration of a veterinarian listening to a baby otter's heartbeat"
```

#### 日本語テキスト入りポスター

```bash
$CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py \
  "A minimalist editorial poster with the exact title \"腹落ちDMARC\" in large serif Japanese font at the top, dark navy background, subtle terminal motif" \
  --size 1024x1536 --quality high
```

#### 透過 PNG が必要な場合

gpt-image-2 は透過背景に対応していません。以下のいずれかを使ってください:

1. **後処理で切り抜く(推奨、gpt-image-2 のテキスト描画/レイアウトの強みを保持)**
   ```bash
   $CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py "minimalist fox logo on plain white background"
   rembg i generated_images/<画像>.png generated_images/<画像>_alpha.png
   ```
2. **`gpt-image-1.5` に切替(透過対応の旧モデル)**
   ```bash
   $CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py \
     "minimalist fox logo, flat vector, navy and gold" \
     --model gpt-image-1.5 --background transparent --output-format png
   ```
3. **姉妹スキル `ccskill-nanobanana` を使う**

#### 参照画像をベースに編集(背景置換)

```bash
$CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py \
  "Place the same fox logo on a deep navy background with subtle gold sparkles, ready for use as a hero image. Preserve the fox's pose and proportions from the reference." \
  --reference ./logo.png --quality medium
```

> **入力画像の忠実度について**: gpt-image-2 は **常に自動で最大忠実度** で入力画像を処理するため、`input_fidelity` パラメータは指定不要(指定すると 400 エラー)。これは欠落ではなく自動仕様。構図保持はプロンプト内で「Preserve the … from the reference」と書くだけで十分強く効きます。トレードオフは編集時の入力画像トークンが多くなる(コスト増)ことなので、**不要な参照画像は渡さない** のがコスト最適化のコツ。

#### 複数参照を合成

```bash
$CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py \
  "Photorealistic gift basket on white, labeled 'Relax & Unwind', containing all items" \
  --reference ./body-lotion.png --reference ./bath-bomb.png --reference ./soap.png
```

#### マスク編集(inpainting)

```bash
$CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py \
  "A sunlit indoor lounge area with a pool containing a flamingo" \
  --reference ./lounge.png --mask ./mask.png
```

> マスクの透明部分が置換対象。プロンプトには **新しい完全な画像全体** を記述する(消した部分だけではない)。

## プロンプト設計ガイド (gpt-image-2 向けベストプラクティス)

> 一次資料: [OpenAI Image generation guide](https://developers.openai.com/api/docs/guides/image-generation), [gpt-image-2 model page](https://developers.openai.com/api/docs/models/gpt-image-2)

gpt-image-2 は **業界初の Agentic 画像生成モデル** で、画像を生成する前に構造を能動的にリサーチ・計画・推論します。タグ羅列ではなく **クリエイティブディレクターの指示書** のようなプロンプトが最大の効果を発揮します。

### 構造化テンプレ

```
[Subject] / [Style] / [Composition] / [Lighting] / [Details] / [Constraints]
```

**悪い例**: `cute cat`

**良い例**:
```
A gray tabby kitten (subject) /
flat vector illustration, Japanese children's book style (style) /
centered, rule of thirds, medium shot (composition) /
soft morning light, warm tones (lighting) /
wearing a tiny red scarf, holding a yellow star (details) /
white background, no text (constraints)
```

### テキスト描画(gpt-image-2 の最大の強み)

画像内にテキストを入れたい時は **引用符で厳密に囲う**:

```
...poster with the exact title "腹落ちDMARC" in large serif Japanese font at the top,
and the subtitle "Email Authentication for SaaS" in smaller English sans-serif below.
```

gpt-image-2 は多言語テキスト、特に **日本語(漢字/かな)・絵文字の混在表現** が大幅に強化されています。日本語ポスター・SNS バナー・スライド見出しが一発で読める品質で出ます。

### 否定形ではなく肯定形で

| ❌ 悪い | ✅ 良い |
|---|---|
| `a room without furniture` | `an empty room with bare walls and polished concrete floor` |
| `no text` | `clean illustrated background, decorative only` |

モデルは「〜ではない」より「〜である」を正確に反映します。

### 編集時は「保持するもの」を明示

```
Preserve the woman's face, hair, and pose exactly as in the reference.
Replace only the background with a neon Tokyo street at night.
```

> gpt-image-2 は **常に自動で最大忠実度** で入力画像を処理するので、`input_fidelity` パラメータの指定は不要(指定するとエラー)。**プロンプト内で「保持したい要素」を文章で明示** すれば、自動高忠実度処理と組み合わさって構図保持はかなり強く効きます。

### Agentic 推論を活かす「ゴール伝達型」プロンプト

gpt-image-2 は内部で計画・推論するため、**最終的に達成したいゴールを伝える** のが有効です。

| ❌ 手順指示型 | ✅ ゴール伝達型 |
|---|---|
| `draw a bar chart of 4 bars with values 10 20 30 40 colored blue` | `Create an infographic comparing Q1-Q4 revenue (10, 20, 30, 40 million yen) for a board deck. Use a clean dark tech aesthetic with neon blue accents. Include title, axis labels, and value labels on each bar.` |

### スタイル指定は固有名詞より視覚特徴の分解で

版権リスクを避け再現性を上げるため、`Studio Ghibli風` より `hand-painted watercolor, soft pastel palette, cel-shaded` のように視覚的特徴を分解します。

### `revised_prompt` を観察する

レスポンスにはモデルが内部で書き換えた `revised_prompt` が含まれることがあり、本スキルは stdout に `[Revised] ...` として出力 + メタデータ JSON にも保存します。Claude は次の生成ターンでこれを見て、より精緻なプロンプトを組み立て直すフィードバックループを使えます。

## コスト最適化

実装/テスト時は `--quality low` を使う($0.006/枚)。本番出力は `medium`($0.053) または `high`($0.211)。

**非自明なコスト罠**: `1024×1536`(縦長) の `high` は `$0.165` で、**正方形 `1024×1024` の `high`($0.211) より安い**。ポートレート用途は意図的に縦長を選ぶとコストが下がります。

| 品質 | 1024×1024 | 1024×1536 | 1536×1024 |
|---|---|---|---|
| low | $0.006 | $0.011 | $0.011 |
| medium | $0.053 | $0.080 | $0.079 |
| high | $0.211 | **$0.165** | $0.210 |

## 用途別ワークフロー(Claude が判断する基準)

ユーザの依頼に対して、Claude は以下のテーブルでパラメータを自動選択します。

| ユーザの意図 | size | quality | background | output-format | 備考 |
|---|---|---|---|---|---|
| ブログ/記事のヒーロー画像 | `1024x1536` | `medium` | `auto` | `webp` (圧縮 80) | 縦長で映える |
| OGP/SNS バナー | `1536x1024` | `high` | `auto` | `png` | 横長、文字くっきり |
| アイコン/ロゴ(透過必要) | `1024x1024` | `high` | — | `png` | gpt-image-2 で生成 → `rembg` で切り抜き、または `--model gpt-image-1.5 --background transparent` |
| ロゴ(白背景許容) | `1024x1024` | `high` | `auto` | `png` | 後で外部ツールで切り抜く前提 |
| 概念図/インフォグラフィック | `1024x1536` | `high` | `auto` | `png` | テキスト多め、ゴール伝達型プロンプト |
| 試行錯誤中 | `1024x1024` | `low` | `auto` | `png` | コスト圧縮 |
| 既存画像の部分修正 | (参照に合わせる) | `high` | `auto` | (参照に合わせる) | `--reference` + プロンプトで保持要素明示(自動高忠実度なので強い) |

## 姉妹スキルとの使い分け

| 用途 | 第一選択 | 理由 |
|---|---|---|
| 日本語/漢字テキスト入りポスター | **ccskill-gptimage** | gpt-image-2 のテキスト描画が最強 |
| 概念図/業務インフォグラフィック | **ccskill-gptimage** | Agentic 推論で構造を計画 |
| 既存画像の編集・部分修正 | **ccskill-gptimage** | 入力画像を常に最大忠実度で処理 |
| 写真風/イラスト風の単体ビジュアル | どちらでも | コスト感は近い |
| 透過 PNG (ロゴ・アイコン・スプライト) | どちらでも | gpt-image-2 は不可だが (a) `--model gpt-image-1.5` 切替、(b) `rembg` 後処理、(c) ccskill-nanobanana のいずれも実用 |
| 4K 出力 | ccskill-nanobanana | gpt-image-2 は 2K まで |

## 出力ファイル

各画像と並列に **メタデータ JSON サイドカー**(`{画像名}.{ext}.json`)が保存されます。プロンプト・revised_prompt・パラメータ・タイムスタンプを含み、後で再現/微調整するときに使います。

## 制約

- **Organization Verification 必須**(未検証なら 403)
- **透過背景 (`background: transparent`) 非対応** — 指定すると 400。透過が必要なら `--model gpt-image-1.5` か rembg 後処理
- **`input_fidelity` は指定不要(常に最大忠実度で動作)** — 指定すると 400。これは欠落ではなく自動仕様
- 編集時の入力画像トークンが多くなりやすい(自動高忠実度処理のトレードオフ) — 不要な参照画像は渡さない
- レート制限: Tier 1 で 5 IPM(本番運用は Tier 3+ 推奨)
- タイムアウト: 高品質・複雑プロンプトは最大 2 分
- Function calling / Structured outputs 非対応
- レスポンスは `b64_json` のみ(URL は返らない)

## トラブルシューティング

- 403 Forbidden → Org Verification を確認
- レート超過 → Tier を上げる、または `--quality low` で間引く
- タイムアウト → ネットワーク確認、SDK のタイムアウトを 120 秒以上に
- 日本語が崩れる → 引用符 `" "` で正確に囲む、フォント指定(`serif Japanese font` 等)を明示
