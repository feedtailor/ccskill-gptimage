# GPT Image 2 API 完全ガイド

2026年4月21日にOpenAIが正式リリースした、画像生成の新フラッグシップモデル `gpt-image-2`(ChatGPT Images 2.0)の技術詳細です。

## 1. モデル概要

ChatGPT Images 2.0は、state-of-the-artな画像生成モデルで、改善されたテキストレンダリング、多言語対応、高度な視覚推論を特徴としています。これはOpenAIがO系列の推論能力を画像モデルに統合した最初の試みで、画像生成前に構造を能動的にリサーチ・計画・推論する、業界初の真のAgentic画像生成モデルと位置付けられています。

| 項目 | 値 |
|------|------|
| モデルID | `gpt-image-2` |
| スナップショット | `gpt-image-2-2026-04-21` |
| 入力 | テキスト / 画像 |
| 出力 | 画像のみ |
| 最大解像度 | 2K |
| エンドポイント | `/v1/images/generations`, `/v1/images/edits`, `/v1/responses`(tool) |
| Streaming | サポート(partial images) |
| Function calling / Structured outputs | 非対応 |

レート制限は Tier 1 で 100,000 TPM / 5 IPM、Tier 5 で 8,000,000 TPM / 250 IPM。**Organization Verification が必須**である点に注意してください。

---

## 2. 2つのAPIアクセス経路

### 2-1. Image API(単発生成向け)

単発の生成・編集ならこちらがシンプルで高速です。

```python
from openai import OpenAI
import base64

client = OpenAI()

result = client.images.generate(
    model="gpt-image-2",
    prompt="A children's book drawing of a veterinarian listening to a baby otter's heartbeat",
    size="1024x1024",
    quality="high",
    background="transparent",
    output_format="png",
    n=1,
)

image_bytes = base64.b64decode(result.data[0].b64_json)
with open("otter.png", "wb") as f:
    f.write(image_bytes)
```

cURL での最小例:

```bash
curl -X POST "https://api.openai.com/v1/images/generations" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-image-2",
    "prompt": "a minimalist logo of a fox, flat vector, navy and gold",
    "size": "1024x1024",
    "quality": "high"
  }' | jq -r '.data[0].b64_json' | base64 --decode > out.png
```

### 2-2. Responses API(会話・反復編集向け)

マルチターンで画像を育てていくワークフローは Responses API を使います。`image_generation` ツール経由で呼び出し、`previous_response_id` で文脈を繋げます。

```python
from openai import OpenAI
import base64

client = OpenAI()

# 1ターン目: 生成
resp = client.responses.create(
    model="gpt-5",   # mainlineのモデルから画像ツールを呼び出す
    input="Generate an image of a gray tabby cat hugging an otter with an orange scarf",
    tools=[{"type": "image_generation"}],
)

img_calls = [o for o in resp.output if o.type == "image_generation_call"]
with open("v1.png", "wb") as f:
    f.write(base64.b64decode(img_calls[0].result))

# 2ターン目: 前のレスポンスを継承して編集
resp2 = client.responses.create(
    model="gpt-5",
    previous_response_id=resp.id,
    input="Now make it look photorealistic, golden hour lighting",
    tools=[{"type": "image_generation"}],
)
```

Responses API 限定で使える `action` パラメータ(`auto` / `generate` / `edit`)で生成と編集を明示的に制御できます。通常は `auto` 推奨。

---

## 3. 主要パラメータ徹底解説

### 3-1. `size` と `quality`

| quality | 1024×1024 | 1024×1536 | 1536×1024 |
|---------|----------|----------|----------|
| low     | 272 tok  | 408 tok  | 400 tok  |
| medium  | 1,056 tok | 1,584 tok | 1,568 tok |
| high    | 4,160 tok | 6,240 tok | 6,208 tok |

`auto` にするとモデルがプロンプトに応じて最適選択します。**コスト最適化の第一手段はここ**です。

### 3-2. `output_format` と `output_compression`

- `png`(デフォルト)/ `jpeg` / `webp`
- `jpeg`/`webp` では `output_compression=0-100` で圧縮率指定
- **レイテンシ重視なら `jpeg`**(PNGより速い)

### 3-3. `background`(透過)

> ⚠️ **訂正(2026-04-23 実 API で確認)**: gpt-image-2 は `background: transparent` を**サポートしていません**(400 `Transparent background is not supported for this model.`)。`auto` / `opaque` のみ有効です。透過 PNG が必要な場合は以下のいずれか:
> 1. **`gpt-image-1.5` に切替** — 旧モデルだが透過 PNG/WebP のために現役。OpenAI Cookbook も同モデルを推奨
> 2. **生成後に背景除去** — `rembg` / Photoshop / Remove.bg API などで後処理(gpt-image-2 のテキスト描画やレイアウトの強みを活かしたい場合)
> 3. **`ccskill-nanobanana`(Gemini 3 Pro Image)を使う**

### 3-4. `input_fidelity`(入力保持忠実度)

> ⚠️ **訂正(2026-04-23 実 API で確認 + Web Claude 経由で OpenAI ドキュメント再確認)**:
>
> gpt-image-2 では `input_fidelity` を指定すると 400 エラーになる(`The model 'gpt-image-2' does not support the 'input_fidelity' parameter.`)が、これは **「機能が削除された」のではなく「常に自動で最大忠実度で処理する仕様」** であるため。パラメータ自体が不要。
>
> つまり gpt-image-2 では編集時の入力画像保持は **常に最高設定で動作している**(構図保持の精度はむしろ強い)。トレードオフとして **編集時の画像入力トークンが増えやすい(コスト増)** ので、不要な参照画像を渡さないことがコスト最適化のポイント。
>
> 旧モデル `gpt-image-1.5` を `--model gpt-image-1.5` で使う場合は引き続き `input_fidelity: high|low` で制御可能。

### 3-5. `moderation`

- `auto`(デフォルト): 標準的フィルタリング
- `low`: 緩めのフィルタリング(要件に応じて)

### 3-6. `partial_images`(ストリーミング)

0〜3の数値で、生成途中の部分画像を受け取れます。1枚あたり**+100トークン**のコストがかかります。

```python
stream = client.images.generate(
    model="gpt-image-2",
    prompt="...",
    stream=True,
    partial_images=2,
)
for event in stream:
    if event.type == "image_generation.partial_image":
        # event.partial_image_index, event.b64_json
        ...
```

---

## 4. 画像編集・マスキング(inpainting)

### 複数参照画像からの合成

```python
result = client.images.edit(
    model="gpt-image-2",
    image=[
        open("body-lotion.png", "rb"),
        open("bath-bomb.png", "rb"),
        open("soap.png", "rb"),
    ],
    prompt="Photorealistic gift basket on white, labeled 'Relax & Unwind', containing all items",
    # gpt-image-2 は input_fidelity を受け付けない(常に最大忠実度・3-4 節参照)
    # 旧モデル gpt-image-1.5 を使う場合のみ input_fidelity="high" を指定可能
)
```

### マスク指定(部分編集)

```python
result = client.images.edit(
    model="gpt-image-2",
    image=open("lounge.png", "rb"),
    mask=open("mask.png", "rb"),      # 透明部分が置換対象
    prompt="A sunlit indoor lounge area with a pool containing a flamingo",
)
```

**マスクの要件**:
- 元画像と同じフォーマット・サイズ
- 50MB未満
- アルファチャネル必須(透明部分が編集対象)
- プロンプトには**新しい完全な画像全体**を記述する(消した部分だけではない)

**重要 — マスクは「真の inpainting」ではない**(OpenAI 公式ガイド原文):

> Masking with GPT Image is entirely prompt-based. The model uses the mask as guidance, but may not follow its exact shape with complete precision.

つまり edits API は **マスクの有無に関わらず常に全画面を再描画** する。マスク外の領域も「常時最大忠実度」のおかげで非常によく保持されるが、ピクセル単位で同一になる保証はない。**ピクセル単位の完全保持が必要なら Pillow 等で対象領域だけクロップ→編集→ペーストバックするハイブリッド方式が唯一の手段**。

実用上は、UI スクリーンショットの一部差し替え程度であれば「`Preserve absolutely everything else exactly as in the reference: <要素を列挙>`」のように保持要素を具体的に書き並べると、デバイスシリアル番号レベルの細部まで再現される(2026-04-23 dogfooding 検証済み、`docs/dogfooding-log.md`)。

---

## 5. 料金体系

トークン課金モデルで、内訳は以下の通りです(per 1M tokens):

| 種別 | 入力 | キャッシュ入力 | 出力 |
|------|------|----------------|------|
| Text | $5.00 | $1.25 | $10.00 |
| Image | $8.00 | $2.00 | $30.00 |

**1枚あたりの実質コスト目安**(1024×1024):

| quality | コスト |
|---------|--------|
| low | 約 $0.006 |
| medium | 約 $0.053 |
| high | 約 $0.211 |

興味深い点として、1024×1536の高品質は$0.165で、標準の1024×1024高品質($0.211)より安いので、ポートレート用途ではあえて縦長にするのがコスト的に有利です。

---

## 6. プロンプトのベストプラクティス

### 6-1. 構造化プロンプトの推奨テンプレ

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

### 6-2. テキストレンダリングのコツ

画像内にテキストを入れたい時は **引用符で厳密に囲う**:

```
...poster with the exact title "腹落ちDMARC" in large serif Japanese font at the top,
and the subtitle "Email Authentication for SaaS" in smaller English sans-serif below.
```

gpt-image-2は多言語テキスト、特に日本語・漢字・かな・絵文字の混在表現が大幅に強化されています。

### 6-3. 否定形ではなく肯定形で

❌ `a room without furniture`
✅ `an empty room with bare walls and polished concrete floor`

モデルは「〜ではない」より「〜である」を正確に反映します。

### 6-4. 編集時は「保持するもの」を明示

```
Keep the woman's face, hair, and pose exactly as in the reference.
Replace only the background with a neon Tokyo street at night.
```

gpt-image-2 は入力画像を常に最大忠実度で処理するため、明示的に「保持するもの」を書くだけで強い再現性が得られます(`input_fidelity` パラメータの指定は不要、3-4 節参照)。

### 6-5. Agentic推論を活かす使い方

gpt-image-2は内部で計画・推論するため、**最終的に達成したいゴールを伝える**のが有効です。

❌ `draw a bar chart of 4 bars with values 10 20 30 40 colored blue`
✅ `Create an infographic comparing Q1-Q4 revenue (10, 20, 30, 40 million yen) for a board deck. Use a clean dark tech aesthetic with neon blue accents. Include title, axis labels, and value labels on each bar.`

### 6-6. スタイル指定は固有名詞より形容的に

版権リスクを避け再現性を上げるため、「Studio Ghibli風」より「hand-painted watercolor, soft pastel palette, cel-shaded」のように**視覚的特徴の分解**を推奨。

### 6-7. Revised Promptを観察する

Responses APIでは内部で自動書き換えされた `revised_prompt` が返ります。これを次回のプロンプト改善のフィードバックループに使うと品質が安定します。

```python
call = [o for o in resp.output if o.type == "image_generation_call"][0]
print(call.revised_prompt)  # モデルが実際に解釈したプロンプト
```

---

## 7. 運用上の落とし穴

- **レイテンシ**: 高品質・複雑プロンプトは最大2分かかることがある。タイムアウトは長めに(120秒以上推奨)
- **一貫性**: キャラクターやブランド要素の同一性は、複数生成間で微妙に揺れる → seed相当の機構はないため、input_fidelity + リファレンス画像で補う
- **レイアウト制御**: 厳密な座標指定は苦手。UI/スライドレイアウトはマスク併用か、構造化プロンプトで段階的に
- **Tier制限**: Tier 1は5 IPMなので、本番バッチ投入は Tier 3以上が現実的
- **`gpt-image-1.5`はデフォルトから降格したがAPIでは利用可能**。旧ワークフロー互換用に残されている

---

## 8. espar 文脈でのユースケース提案

Oishiの事業文脈だと、以下が即効性あると思います:

- **espar press/vault**: ブログ記事のヒーロー画像を `quality:medium` + 1024×1536 で $0.041/枚 で量産
- **DMARC advisory コンテンツ**: 「腹落ちDMARC」シリーズのアイキャッチを、dark tech/ターミナル風に統一したスタイルプロンプトをテンプレ化
- **micss.biz**: MDM設定の概念図・フロー図を、gpt-image-2の強化されたテキスト描画で生成(従来は外部図解ツールが必要だった領域)
- **Claude Code チュータリング教材**: スクリーンショット + 注釈の合成を `image_edit` + マスクで半自動化

公式ドキュメントの[Image generation guide](https://developers.openai.com/api/docs/guides/image-generation)と[gpt-image-2モデルページ](https://developers.openai.com/api/docs/models/gpt-image-2)が一次情報源として最も正確です。