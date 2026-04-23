# research-notes #015 (cookbook): OpenAI Cookbook 原文保全ノート

**出典**: [GPT Image Generation Models Prompting Guide](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide)(2026-04-23 取得、WebFetch × 12 回に分割)

本ノートは Cookbook の目次構造・原則セクション・全ユースケースのプロンプト例を**原文引用で保全**したもの。SKILL.md 刷新(Phase 2b: progressive disclosure 構成)の一次資料ベースとして使用する。

---

## 目次

1. [Section 1: Introduction](#section-1-introduction)
2. [Section 2: Prompting Fundamentals](#section-2-prompting-fundamentals)
3. [Section 4: Generate ユースケース(10 件)](#section-4-generate-ユースケース)
4. [Section 5: Edit ユースケース(9 件)](#section-5-edit-ユースケース)
5. [Section 6: Additional High-Value Use Cases(4 件)](#section-6-additional-high-value-use-cases)
6. [メモ: Cookbook と現 SKILL の乖離ポイント](#cookbook-と現-skill-の乖離ポイント)

---

## Section 1: Introduction

### 1.1 Model Summary(原文表を転記)

| Model | outputQuality | input_fidelity | Resolutions | Recommended Use |
|---|---|---|---|---|
| `gpt-image-2` | low, medium, high | Disabled | Any resolution per constraints | Recommended default; highest-quality generation/editing |
| `gpt-image-1.5` | low, medium, high | low, high | 1024x1024, 1024x1536, 1536x1024, auto | Legacy; keep for validation during migration |
| `gpt-image-1` | low, medium, high | low, high | 1024x1024, 1024x1536, 1536x1024, auto | Legacy compatibility only |
| `gpt-image-1-mini` | low, medium, high | low, high | 1024x1024, 1024x1536, 1536x1024, auto | Cost-constrained batches; rapid ideation |

**重要な示唆**(現 SKILL との差異):
- gpt-image-2 は **"Any resolution per constraints"** と記載 — 現 `generate_image.py` は `SIZE_CHOICES = ["auto", "1024x1024", "1024x1536", "1536x1024"]` で固定している。Cookbook の Section 4.10 は `1536x864` を使っており、fixed choice が実装上の足枷になっている可能性。

### 1.1 When to Use Which Model(原文引用)

> "Choose `gpt-image-2` as the default for most production workflows. It is the strongest overall model and the right upgrade target for teams currently using `gpt-image-1.5` or `gpt-image-1`"

> "Choose `gpt-image-2` with quality: low when speed and unit economics dominate the decision."

> "Keep `gpt-image-1.5` or `gpt-image-1` only for backward compatibility while you validate prompt migrations, regression-test outputs, or maintain older workflows that are not yet ready to move."

### 1.1 Recommended Upgrade Path(原文引用)

> "Upgrade to `gpt-image-2` for customer-facing assets, photorealistic generation, editing-heavy flows, brand-sensitive creative, text-in-image work"

> "Consider `gpt-image-1-mini` instead of legacy models only when the main goal is lowering cost for large batches"

> "During migration, keep prompts largely the same at first, then retune only after you have compared output quality"

---

## Section 2: Prompting Fundamentals

**10 原則の完全原文**(見出しは Cookbook 原文、本文も省略なし):

### Structure + Goal

> "Write prompts in a consistent order (background/scene → subject → key details → constraints) and include the intended use (ad, UI mock, infographic) to set the 'mode' and level of polish. For complex requests, use short labeled segments or line breaks instead of one long paragraph."

### Prompt Format

> "Use the format that is easiest to maintain. Minimal prompts, descriptive paragraphs, JSON-like structures, instruction-style prompts, and tag-based prompts can all work well as long as the intent and constraints are clear."

### Specificity + Quality Cues

> "Be concrete about materials, shapes, textures, and the visual medium (photo, watercolor, 3D render), and add targeted 'quality levers' only when needed. For photorealism, include the word 'photorealistic' directly in the prompt to strongly engage the model's photorealistic mode."

### Latency vs Fidelity

> "For latency-sensitive or high-volume use cases, start with `quality='low'` and evaluate whether it meets your visual requirements. For small or dense text, detailed infographics, close-up portraits, and high-resolution outputs, compare `medium` or `high` before shipping."

### Composition

> "Specify framing and viewpoint (close-up, wide, top-down), perspective/angle (eye-level, low-angle), and lighting/mood (soft diffuse, golden hour, high-contrast) to control the shot. If layout matters, call out placement (e.g., 'logo top-right,' 'subject centered')."

### People, Pose, and Action

> "For people in scenes, describe scale, body framing, gaze, and object interactions. Examples: 'full body visible, feet included,' 'child-sized relative to the table,' 'looking down at the open book, not at the camera.'"

### Constraints (What to Change vs Preserve)

> "State exclusions and invariants explicitly (e.g., 'no watermark,' 'preserve identity/geometry/layout'). For edits, use 'change only X' + 'keep everything else the same,' and repeat the preserve list on each iteration to reduce drift."

### Text in Images

> "Put literal text in **quotes** or **ALL CAPS** and specify typography details (font style, size, color, placement) as constraints. For tricky words, spell them out letter-by-letter to improve character accuracy. Use `medium` or `high` quality for small text and dense information panels."

### Multi-Image Inputs

> "Reference each input by **index and description** ('Image 1: product photo… Image 2: style reference…') and describe how they interact ('apply Image 2's style to Image 1'). When compositing, be explicit about which elements move where."

### Iterate Instead of Overloading

> "Long prompts can work well, but debugging is easier when you start with a clean base prompt and refine with small, single-change follow-ups ('make lighting warmer,' 'remove the extra tree'). Use references like 'same style as before' to leverage context, but re-specify critical details if they start to drift."

---

## Section 4: Generate ユースケース

すべて `gpt-image-2`、特記なければ `images.generate`(入力画像なし)、`size=1024x1536`、`quality=medium`。

### 4.1 Infographics

**用途**: "Use infographics to explain structured information for a specific audience: students, executives, customers, or the general public."

**品質指針**: "For dense layouts or heavy in-image text, it's recommended to set output generation quality to 'high'."

**プロンプト原文**:
```
Create a detailed Infographic of the functioning and flow of an automatic coffee machine like a Jura.
From bean basket, to grinding, to scale, water tank, boiler, etc.
I'd like to understand technically and visually the flow.
```

### 4.2 Translation in Images(edit 経路)

**用途**: "Used for localizing existing designs (ads, UI screenshots, packaging, infographics) into another language without rebuilding the layout from scratch."

**重要制約原文**:
> "The key is to preserve everything except the text—keep typography style, placement, spacing, and hierarchy consistent—while translating verbatim and accurately, with no extra words, no reflow unless necessary, and no unintended edits to logos, icons, or imagery."

**プロンプト原文**:
```
Translate the text in the infographic to Spanish. Do not change any other aspect of the image.
```

**設定**: `images.edit`、入力画像 1 枚。

### 4.3 Photorealistic Images that Feel "natural"

**用途**: "To get believable photorealism, prompt the model as if a real photo is being captured in the moment. Use photography language (lens, lighting, framing) and explicitly ask for real texture (pores, wrinkles, fabric wear, imperfections). Avoid words that imply studio polish or staging. When detail matters, set quality='high'."

**プロンプト原文**:
```
Create a photorealistic candid photograph of an elderly sailor standing on a small fishing boat.
He has weathered skin with visible wrinkles, pores, and sun texture, and a few faded traditional sailor tattoos on his arms.
He is calmly adjusting a net while his dog sits nearby on the deck. Shot like a 35mm film photograph, medium close-up at eye level, using a 50mm lens.
Soft coastal daylight, shallow depth of field, subtle film grain, natural color balance.
The image should feel honest and unposed, with real skin texture, worn materials, and everyday detail. No glamorization, no heavy retouching.
```

### 4.4 World knowledge

**用途**: "GPT image generation models can pair strong reasoning with world knowledge. For example, when asked to generate a scene set in Bethel, New York in August 1969, they can infer Woodstock and produce an accurate, context-appropriate image without being explicitly told about the event."

**プロンプト原文**:
```
Create a realistic outdoor crowd scene in Bethel, New York on August 16, 1969.
Photorealistic, period-accurate clothing, staging, and environment.
```

### 4.5 Logo Generation

**用途**: "Strong logo generation comes from clear brand constraints and simplicity. Describe the brand's personality and use case, then ask for a clean, original mark with strong shape, balanced negative space, and scalability across sizes."

**補足**: "You can specify parameter 'n' to denote the number of variations you would like to generate."

**プロンプト原文**:
```
Create an original, non-infringing logo for a company called Field & Flour, a local bakery.
The logo should feel warm, simple, and timeless. Use clean, vector-like shapes, a strong silhouette, and balanced negative space.
Favor simplicity over detail so it reads clearly at small and large sizes. Flat design, minimal strokes, no gradients unless essential.
Plain background. Deliver a single centered logo with generous padding. No watermark.
```

**設定**: `n=4`(4 バリエーション生成)。

### 4.6 Ads Generation

**用途**: 広告は技術仕様ではなく**クリエイティブブリーフ**として書く。ブランド・オーディエンス・概念・構成・正確なコピーを記述し、モデルに創造的判断を委ねる。

**プロンプト原文**:
```
Give me a cool in culture ad / fashion shot for a brand called Thread.
It's a hip young street brand. The ad shows a group of friends hanging out together with the tagline "Yours to Create."
Make it feel like a polished campaign image for a youth streetwear audience: stylish, contemporary, energetic, and tasteful.
Use clean composition, strong color direction, natural poses, and premium fashion photography cues.
Render the tagline exactly once, clearly and legibly, integrated into the ad layout.
No extra text, no watermarks, no unrelated logos.
```

### 4.7 Story-to-Comic Strip

**用途**: 物語を複数パネルの漫画に変換。各パネルを具体的・アクション中心の記述で定義し、パネル間の可読性とテンポを維持。

**プロンプト原文**:
```
Create a short vertical comic-style reel with 4 equal-sized panels.
Panel 1: The owner leaves through the front door. The pet is framed in the window behind them, small against the glass, eyes wide, paws pressed high, the house suddenly quiet.
Panel 2: The door clicks shut. Silence breaks. The pet slowly turns toward the empty house, posture shifting, eyes sharp with possibility.
Panel 3: The house transformed. The pet sprawls across the couch like it owns the place, crumbs nearby, sunlight cutting across the room like a spotlight.
Panel 4: The door opens. The pet is seated perfectly by the entrance, alert and composed, as if nothing happened.
```

### 4.8 UI Mockups

**用途**: "Describe as implemented product" — 実装済みの UI として記述し、レイアウト・階層・スペーシング・実 UI 要素に注目、**コンセプトアート用語は避ける**。

**プロンプト原文**:
```
Create a realistic mobile app UI mockup for a local farmers market.
Show today's market with a simple header, a short list of vendors with small photos and categories, a small "Today's specials" section, and basic information for location and hours.
Design it to be practical, and easy to use. White background, subtle natural accent colors, clear typography, and minimal decoration.
It should look like a real, well-designed, beautiful app for a small local market.
Place the UI mockup in an iPhone frame.
```

### 4.9 Scientific / Educational Visuals

**用途**: 生物・化学・クラスボード解説用。フラット科学アイコン・図解・学習用アセット。

**推奨設定**: `size=1536x1024`、**`quality=high`**(密集ラベル・図表向け)。

**プロンプト原文**:
```
Create a simple biology diagram titled "Cellular Respiration at a Glance" for high school students.

Show how glucose turns into energy inside a cell. Include glycolysis, the Krebs cycle, and the electron transport chain.
Use arrows to connect the steps, and label the main molecules: glucose, pyruvate, ATP, NADH, FADH2, CO2, O2, and H2O.
Make it look like a clean classroom handout or slide, with a white background, simple icons, clear labels, and easy-to-read text.

Avoid tiny text, extra decoration, or anything that makes the diagram hard to understand.
```

### 4.10 Slides, Diagrams, Charts, and Productivity Images

**用途**: アーティファクト仕様(スライド・図・チャート)として記述し、**実際のテキスト/データを直接プロンプトに含める**。

**推奨設定**: `size=1536x864`(これまでの 4 区分固定外!)、**`quality=high`**。

**プロンプト原文**:
```
Create one pitch-deck slide titled **"Market Opportunity"** that feels like a real Series A fundraising slide from a YC-backed startup.

Use a clean white background, modern sans-serif typography like Inter, and a crisp, minimal layout. The slide should include:

* A TAM/SAM/SOM concentric-circle diagram in muted blues and grays
* Specific, believable market sizing numbers:

  * **TAM:** $42B
  * **SAM:** $8.7B
  * **SOM:** $340M
* A clean bar chart below showing market growth from **2021 to 2026**, with a subtle upward trend
* Small footnotes: **"AGI Research, 2024"** and **"Internal analysis"**
* A company logo placeholder in the bottom-right corner

The design should look like it belongs in a deck that actually raised money: highly readable text, clear data hierarchy, polished spacing, and professional startup-style visual language.

Avoid clip art, stock photography, gradients, shadows, decorative elements, or anything that feels generic or overdesigned.
```

---

## Section 5: Edit ユースケース

すべて `gpt-image-2`、`images.edit`、特記なければ `size=1024x1536`、`quality=medium`。

### 5.1 Style Transfer

**用途**: 参照画像のビジュアル言語(パレット・テクスチャ・筆致)を別コンテンツに適用。

**プロンプト原文**:
```
Use the same style from the input image and generate a man riding a motorcycle on a white background.
```

**入力**: 1 枚(reference style image)。

### 5.2 Virtual Clothing Try-On

**用途**: 人物のアイデンティティ保持しつつ服だけ置換。顔・体型・ポーズは厳格ロック。

**プロンプト原文**:
```
Edit the image to dress the woman using the provided clothing images. Do not change her face, facial features, skin tone, body shape, pose, or identity in any way. Preserve her exact likeness, expression, hairstyle, and proportions. Replace only the clothing, fitting the garments naturally to her existing pose and body geometry with realistic fabric behavior. Match lighting, shadows, and color temperature to the original photo so the outfit integrates photorealistically, without looking pasted on. Do not change the background, camera angle, framing, or image quality, and do not add accessories, text, logos, or watermarks.
```

**入力**: 5 枚(人物 1 + 衣装 4)。

### 5.3 Drawing → Image (Rendering)

**用途**: ラフスケッチを写真的リアリズムに変換。レイアウト・遠近法を保持、新要素は追加しない。

**プロンプト原文**:
```
Turn this drawing into a photorealistic image.
Preserve the exact layout, proportions, and perspective.
Choose realistic materials and lighting consistent with the sketch intent.
Do not add new elements or text.
```

**入力**: 1 枚(sketch)。

### 5.4 Product Mockups

**用途**: 商品抽出・背景除去。エッジ品質とラベル可読性の保持。

**プロンプト原文**:
```
Extract the product from the input image and place it on a plain white opaque background.
Output: centered product, crisp silhouette, no halos/fringing.
Preserve product geometry and label legibility exactly.
Add only light polishing and a subtle realistic contact shadow.
Do not restyle the product; only remove background and lightly polish.
```

**入力**: 1 枚。**`background=opaque`** 明示。

### 5.5 Marketing Creatives with Real Text In-Image

**用途**: 広告素材に実テキストを組み込む。タイポ制約を明示的に、verbatim rendering を要求。

**プロンプト原文**:
```
Create a realistic billboard mockup of the shampoo on a highway scene during sunset.
Billboard text (EXACT, verbatim, no extra characters):
"Fresh and clean"
Typography: bold sans-serif, high contrast, centered, clean kerning.
Ensure text appears once and is perfectly legible.
No watermarks, no logos.
```

**入力**: 1 枚(シャンプーボトル)。

### 5.6 Lighting and Weather Transformation

**用途**: 写真の時間帯・季節・天候を変更し、構図・アイデンティティ・ジオメトリ・カメラアングル・オブジェクト配置は保持。

**プロンプト原文**:
```
Make it look like a winter evening with snowfall.
```

**入力**: 1 枚(5.5 で生成した billboard 画像)。**Cookbook は `input_fidelity=high` 指定**(gpt-image-2 では自動処理されるため不要/エラー扱い。Cookbook の記述が旧モデル前提を引きずっている例)。

### 5.7 Object Removal

**用途**: 特定要素だけ削除、他要素(人物の身元・照明・背景)は完全保持。

**プロンプト原文**:
```
Remove the flower from man's hand. Do not change anything else.
```

**入力**: 1 枚。Cookbook は `input_fidelity=high`(gpt-image-2 では上記同様)。

### 5.8 Insert the Person Into a Scene

**用途**: 人物を新シーンに合成。ストーリーボード・キャンペーン制作向け。

**プロンプト原文**:
```
Generate a highly realistic action scene where this person is running away from a large, realistic brown bear attacking a campsite. The image should look like a real photograph someone could have taken, not an overly enhanced or cinematic movie-poster image.
She is centered in the image but looking away from the camera, wearing outdoorsy camping attire, with dirt on her face and tears in her clothing. She is clearly afraid but focused on escaping, running away from the bear as it destroys the campsite behind her.
The campsite is in Yosemite National Park, with believable natural details. The time of day is dusk, with natural lighting and realistic colors. Everything should feel grounded, authentic, and unstyled, as if captured in a real moment. Avoid cinematic lighting, dramatic color grading, or stylized composition.
```

**入力**: 1 枚(人物ソース)。

### 5.9 Multi-Image Referencing and Compositing

**用途**: 複数入力から要素を合成。どの要素をどこに移植するかを明示、照明・遠近・スケール・影をマッチさせる。

**プロンプト原文**:
```
Place the dog from the second image into the setting of image 1, right next to the woman, use the same style of lighting, composition and background. Do not change anything else.
```

**入力**: 2 枚(Image 1: 基本シーン、Image 2: 移植対象)。

---

## Section 6: Additional High-Value Use Cases

### 6.1 Interior Design "Swap"

**用途**: 室内写真の精密オブジェクト置換。照明・影・カメラアングル・周辺コンテキスト保持。

**推奨設定**: `size=1536x1024`。

**プロンプト原文**:
```
In this room photo, replace ONLY white with chairs made of wood.
Preserve camera angle, room lighting, floor shadows, and surrounding objects.
Keep all other aspects of the image unchanged.
Photorealistic contact shadows and fabric texture.
```

**入力**: 1 枚。

### 6.2 3D Pop-Up Holiday Card

**用途**: 物理的な keepsake として撮影されたようなプレミアム季節マーケティング素材。

**プロンプト原文**:
```
Create a Christmas holiday card illustration.

Scene:
a cozy Christmas scene with an old teddy bear sitting inside a keepsake box,
slightly worn fur, soft stitching repairs, placed near a window with falling snow outside.
The scene suggests the child has grown up, but the memories remain.

Mood:
Warm, nostalgic, gentle, emotional.

Style:
Premium holiday card photography, soft cinematic lighting,
realistic textures, shallow depth of field,
tasteful bokeh lights, high print-quality composition.

Constraints:
- Original artwork only
- No trademarks
- No watermarks
- No logos

Include ONLY this card text (verbatim):
"Merry Christmas — some memories never fade."
```

**入力**: 0 枚(生成)。

### 6.3 Collectible Action Figure / Plush Keychain

**用途**: マーチ企画向けのプレミアム玩具撮影。素材感・パッケージ・印刷鮮明さを重視。

**プロンプト原文**(Python f-string テンプレートとして):
```python
prompt = f"""
Create a collectible action figure of {character_description}, in blister packaging.

Concept:
A nostalgic holiday collectible inspired by the simple toy airplanes
children used to play with during winter holidays.
Evokes warmth, imagination, and childhood wonder.

Style:
Premium toy photography, realistic plastic and painted metal textures,
studio lighting, shallow depth of field,
sharp label printing, high-end retail presentation.

Constraints:
- Original design only
- No trademarks
- No watermarks
- No logos

Include ONLY this packaging text (verbatim):
"{short_copy}"
"""
```

**入力**: 0 枚(生成)。

### 6.4 Children's Book Art with Character Consistency

**用途**: 物語シーン間でキャラクター外観を維持する複数画像ワークフロー。**Anchor 画像を最初に生成し、後続シーンは edit で継続**。

#### Part 1 — Character Anchor

```python
prompt = """
Create a children's book illustration introducing a main character.

Character:
A young, storybook-style hero inspired by a little forest outlaw,
wearing a simple green hooded tunic, soft brown boots, and a small belt pouch.
The character has a kind expression, gentle eyes, and a brave but warm demeanor.
Carries a small wooden bow used only for helping, never harming.

Theme:
The character protects and rescues small forest animals like squirrels, birds, and rabbits.

Style:
Children's book illustration, hand-painted watercolor look,
soft outlines, warm earthy colors, whimsical and friendly.
Proportions suitable for picture books (slightly oversized head, expressive face).

Constraints:
- Original character (no copyrighted characters)
- No text
- No watermarks
- Plain forest background to clearly showcase the character
"""
```

#### Part 2 — Story Continuation(edit 経路、anchor を入力)

```python
prompt = """
Continue the children's book story using the same character.

Scene:
The same young forest hero is gently helping a frightened squirrel
out of a fallen tree after a winter storm.
The character kneels beside the squirrel, offering reassurance.

Character Consistency:
- Same green hooded tunic
- Same facial features, proportions, and color palette
- Same gentle, heroic personality

Style:
Children's book watercolor illustration,
soft lighting, snowy forest environment,
warm and comforting mood.

Constraints:
- Do not redesign the character
- No text
- No watermarks
"""
```

**入力**: Part 1 = 0 枚、Part 2 = 1 枚(Part 1 の成果物を `.edit()` に渡す)。

---

## Cookbook と現 SKILL の乖離ポイント

Phase 2b SKILL 刷新時に**明示的に解消/反映すべき**項目:

| # | 項目 | Cookbook の実態 | 現 SKILL 実装/記述 | 対応方針 |
|---|---|---|---|---|
| 1 | 解像度の自由度 | gpt-image-2 は "Any resolution per constraints"、Section 4.10 で `1536x864` 使用 | `SIZE_CHOICES` が 4 固定 | `generate_image.py` の choices 緩和を別 issue で検討(本 PR の範囲外) |
| 2 | Section 2 の原則 10 項目 | Structure+Goal / Prompt Format / Specificity+Quality / Latency / Composition / People / Constraints / Text / Multi-Image / Iterate | SKILL.md は 6〜7 原則のみ(People や Multi-Image Inputs は弱い or 無い) | **SKILL.md 骨子に 10 原則を短文で網羅** |
| 3 | `input_fidelity` の Cookbook 例 | 5.6/5.7/5.8/5.9 の edit 例で `input_fidelity=high` を明記 | gpt-image-2 では自動・指定不可 | SKILL.md で「Cookbook の edit 例には `input_fidelity` が出てくるが gpt-image-2 では不要(自動最大)」と**明示的に注記** |
| 4 | ユースケース別プロンプト | 23 件の完成プロンプトを原文で提供 | SKILL.md は 5〜6 件の薄いサンプル | **`prompts/` 配下に分離、Cookbook 原文を出典付き転記** |
| 5 | Multi-Image Inputs の書き方 | "Image 1: product photo… Image 2: style reference…" のインデックス方式が公式推奨 | SKILL.md 側に記載なし | 原則セクションに追加 |
| 6 | People, Pose, and Action | "full body visible, feet included," "looking down at the open book, not at the camera" | SKILL.md に記載なし | 原則セクションに追加 |
| 7 | quality 選択の使い分け | "small or dense text / close-up portraits / infographics → compare medium/high" | 現 SKILL は「試行 low、本番 medium/high」止まり | 原則セクションに Cookbook 原文を引く |
| 8 | Logo 用途の `n` パラメータ | Cookbook は 4.5 で `n=4` を例示 | 現 `generate_image.py` は `n=1` ハードコード | `--n` 追加は別 issue(本 PR の範囲外) |

---

## Phase 2b 設計へ

**ファイル構成案**(progressive disclosure):

```
.claude/skills/ccskill-gptimage/
├── SKILL.md / SKILL.ja.md
│    - Section 2 の 10 原則を骨子として網羅
│    - ユースケース表は各 prompts/*.md への索引のみ
│    - 局所編集・透過などの gptimage 固有制約は本体に残す
├── prompts/
│    ├── README.md               (インデックス)
│    ├── infographics.md         (4.1 + 4.9 + 4.10 を統合)
│    ├── photorealism.md         (4.3 + 4.4 + 4.8 relevant + 5.8)
│    ├── logo.md                 (4.5)
│    ├── ads-marketing.md        (4.6 + 5.5)
│    ├── comic-storyboard.md     (4.7)
│    ├── ui-mockups.md           (4.8)
│    ├── text-in-images.md       (5.5 + 日本語実例)
│    ├── image-translation.md    (4.2)
│    ├── style-transfer.md       (5.1)
│    ├── try-on.md               (5.2)
│    ├── sketch-to-render.md     (5.3)
│    ├── product-mockup.md       (5.4)
│    ├── lighting-weather.md     (5.6)
│    ├── object-removal.md       (5.7)
│    ├── scene-composite.md      (5.8 + 5.9)
│    ├── interior-swap.md        (6.1)
│    ├── holiday-card.md         (6.2)
│    ├── collectible.md          (6.3)
│    └── character-consistency.md (6.4)
```

各 `prompts/*.md` は:
1. **Cookbook 原文プロンプト**(出典 URL + 取得日 + 出典セクション番号を明記)
2. **本スキル CLI での実行例**(`$CCSKILL_GPTIMAGE_DIR/venv/bin/python generate_image.py ...`)に置き換え
3. **gpt-image-2 固有の注意**(`input_fidelity` 不要・透過不可・コスト罠など)を Cookbook 例の横に補足
4. **社内実証ノート**(dogfooding-log.md 関連があれば)を区別して併記

SKILL.md は骨子に 10 原則 + 「このユースケースならこのファイルを読め」の索引表のみ、というコンパクトな構成にする。
