---
name: ccskill-gptimage
description: |
  Skill for image generation needs.
  Generate and edit high-quality images via OpenAI gpt-image-2 (ChatGPT Images 2.0).
  Strong at multilingual text rendering (Japanese included), agentic visual reasoning,
  reference-image fidelity, transparent PNG, and complex infographics.
---

# ccskill-gptimage Image Generation Skill

## Overview

This skill generates and edits images via OpenAI gpt-image-2. **The user only describes intent** — Claude composes the structured prompt, style hints and cost-optimized parameters from conversation history and project context. Sister skill: `ccskill-nanobanana` (Gemini 3 Pro Image); use them based on use case.

## Prerequisites

- Set `CCSKILL_GPTIMAGE_DIR` to this skill's repository path:
  ```bash
  export CCSKILL_GPTIMAGE_DIR="$HOME/projects/ccskill-gptimage"
  ```
- `OPENAI_API_KEY` must be set (or written into `$CCSKILL_GPTIMAGE_DIR/.env`)
- **The OpenAI Organization must be Verified** (unverified orgs get 403)

## Usage

```bash
$CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py "prompt"
```

### Options

| Option | Description | Default | Values |
|---|---|---|---|
| `--size` | Output size | `1024x1024` | `auto` / `1024x1024` / `1024x1536` (portrait) / `1536x1024` (landscape) |
| `--quality` | Quality | `auto` | `auto` / `low` / `medium` / `high` |
| `--background` | Background | `auto` | `auto` / `opaque` (use `--model gpt-image-1.5` for `transparent`) |
| `--output-format` | Output format | `png` | `png` / `jpeg` / `webp` |
| `--output-compression` | Compression (jpeg/webp) | none | 0-100 |
| `--output` | Output directory | `./generated_images` | any path |
| `--reference` | Reference image (repeatable) | none | image file path |
| `--mask` | Mask image (transparent area is editable; requires `--reference`) | none | image file path |
| `--input-fidelity` | Not needed for gpt-image-2 (always max fidelity). For `gpt-image-1.5` | none | `high` / `low` |
| `--moderation` | Moderation level | `auto` | `auto` / `low` |
| `--model` | Model ID | `gpt-image-2` | any model ID |

### Examples

#### Basic
```bash
$CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py \
  "A children's book illustration of a veterinarian listening to a baby otter's heartbeat"
```

#### Japanese poster
```bash
$CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py \
  "A minimalist editorial poster with the exact title \"腹落ちDMARC\" in large serif Japanese font at the top, dark navy background, subtle terminal motif" \
  --size 1024x1536 --quality high
```

#### When you need transparency

gpt-image-2 has no transparent background support. Pick one of:

1. **Post-process with `rembg`** (recommended — keeps gpt-image-2's text rendering and layout strengths)
   ```bash
   $CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py "minimalist fox logo on plain white background"
   rembg i generated_images/<image>.png generated_images/<image>_alpha.png
   ```
2. **Switch to `gpt-image-1.5`** (the older model that still supports transparency)
   ```bash
   $CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py \
     "minimalist fox logo, flat vector, navy and gold" \
     --model gpt-image-1.5 --background transparent --output-format png
   ```
3. **Use the sister skill `ccskill-nanobanana`**

#### Reference editing
```bash
$CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py \
  "Place the same fox logo on a deep navy background with subtle gold sparkles, ready for use as a hero image. Preserve the fox's pose and proportions from the reference." \
  --reference ./logo.png --quality medium
```

> **About reference fidelity**: gpt-image-2 always processes input images at maximum fidelity automatically — `input_fidelity` is unnecessary (specifying it returns 400). This is a feature, not a missing parameter: reference preservation is in fact strong. Just spell out what to "Preserve … from the reference" in the prompt. The trade-off: input-image tokens add up when editing, so **don't pass unnecessary references**.

#### Multi-reference composition
```bash
$CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py \
  "Photorealistic gift basket on white, labeled 'Relax & Unwind', containing all items" \
  --reference ./body-lotion.png --reference ./bath-bomb.png --reference ./soap.png
```

#### Mask inpainting
```bash
$CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py \
  "A sunlit indoor lounge area with a pool containing a flamingo" \
  --reference ./lounge.png --mask ./mask.png
```

> The transparent area of the mask is what gets replaced. The prompt must describe the **complete final image**, not just the masked region.

## Prompt Design Guide (gpt-image-2 best practices)

> Sources: [OpenAI Image generation guide](https://developers.openai.com/api/docs/guides/image-generation), [gpt-image-2 model page](https://developers.openai.com/api/docs/models/gpt-image-2)

gpt-image-2 is the **first agentic image generation model**: it actively researches, plans and reasons about structure before generating. Prompts written like a creative director's brief work best — not tag-soup.

### Structured prompt template

```
[Subject] / [Style] / [Composition] / [Lighting] / [Details] / [Constraints]
```

### Text rendering (gpt-image-2's flagship strength)

Wrap any text you want rendered in **strict quotation marks**:

```
...poster with the exact title "腹落ちDMARC" in large serif Japanese font at the top,
and the subtitle "Email Authentication for SaaS" in smaller English sans-serif below.
```

Multilingual text (especially Japanese kanji/kana and emoji) is dramatically improved over previous generations.

### Use positive form, not negation

| ❌ | ✅ |
|---|---|
| `a room without furniture` | `an empty room with bare walls and polished concrete floor` |

### When editing, name what to keep

```
Preserve the woman's face, hair, and pose exactly as in the reference.
Replace only the background with a neon Tokyo street at night.
```

> gpt-image-2 always processes input images at maximum fidelity, so `input_fidelity` is unnecessary (and rejected by the API). The combination of automatic high fidelity + explicit "Preserve …" wording yields strong reference preservation.

### Goal-oriented prompts beat step-by-step instructions

Because gpt-image-2 plans internally, telling it the **goal** outperforms scripting the steps:

| ❌ Stepwise | ✅ Goal-oriented |
|---|---|
| `draw a bar chart of 4 bars with values 10 20 30 40 colored blue` | `Create an infographic comparing Q1-Q4 revenue (10, 20, 30, 40 million yen) for a board deck. Clean dark tech aesthetic with neon blue accents. Include title, axis labels and value labels.` |

### Style by visual attributes, not proper nouns

Avoid copyrighted style names. Use `hand-painted watercolor, soft pastel palette, cel-shaded` rather than `Studio Ghibli style`.

### Observe `revised_prompt`

Responses may include a `revised_prompt` (the model's own paraphrase). This skill prints it as `[Revised] ...` and saves it to the metadata sidecar. Use it as a feedback signal to refine the next prompt.

## Cost Optimization

Use `--quality low` ($0.006/image) while iterating; `medium` ($0.053) or `high` ($0.211) for delivery.

**Counter-intuitive**: `1024×1536` (portrait) at `high` is **$0.165** — *cheaper* than `1024×1024` at `high` ($0.211). Pick portrait whenever the use case allows.

| Quality | 1024×1024 | 1024×1536 | 1536×1024 |
|---|---|---|---|
| low | $0.006 | $0.011 | $0.011 |
| medium | $0.053 | $0.080 | $0.079 |
| high | $0.211 | **$0.165** | $0.210 |

## Use case → parameter table

| Intent | size | quality | background | output-format | Notes |
|---|---|---|---|---|---|
| Blog/article hero | `1024x1536` | `medium` | `auto` | `webp` (compression 80) | Portrait reads better |
| OGP/social banner | `1536x1024` | `high` | `auto` | `png` | Sharp text |
| Icon/logo (transparency required) | `1024x1024` | `high` | — | `png` | Generate with gpt-image-2 → `rembg`, or use `--model gpt-image-1.5 --background transparent` |
| Logo (solid background OK) | `1024x1024` | `high` | `auto` | `png` | Cut out background later if needed |
| Infographic | `1024x1536` | `high` | `auto` | `png` | Lots of text; goal-oriented prompt |
| Iterating | `1024x1024` | `low` | `auto` | `png` | Cost control |
| Edit existing | match reference | `high` | `auto` | match reference | `--reference` + spell out what to preserve |

## Sister skill comparison

| Use case | First choice | Reason |
|---|---|---|
| Posters with Japanese/kanji text | **ccskill-gptimage** | Strongest text rendering |
| Business infographics | **ccskill-gptimage** | Agentic reasoning plans structure |
| Editing / partial modification | **ccskill-gptimage** | Always processes input at max fidelity |
| Photo / illustration single visuals | Either | Comparable cost |
| Transparent PNG (logos, icons, sprites) | Either | gpt-image-2 can't, but (a) `--model gpt-image-1.5`, (b) `rembg` post-processing, (c) ccskill-nanobanana all work |
| 4K output | ccskill-nanobanana | gpt-image-2 caps at 2K |

## Output files

Each image is saved alongside a **metadata JSON sidecar** (`{name}.{ext}.json`) containing the prompt, `revised_prompt`, parameters and timestamp — useful for reproduction and refinement.

## Constraints

- **Organization Verification required**
- **No transparent background** (`background: transparent` returns 400). Use `--model gpt-image-1.5` or `rembg` post-processing.
- **`input_fidelity` is unnecessary (always max fidelity)** — specifying returns 400, but this is "always on", not "missing"
- Editing with reference images uses more input-image tokens (trade-off of automatic max fidelity)
- Rate limits: Tier 1 = 5 IPM (production needs Tier 3+)
- Timeout: up to 2 minutes for high quality / complex prompts
- No function calling, no structured outputs
- Response is `b64_json` only (no URLs)

## Troubleshooting

- 403 Forbidden → check Org Verification
- Rate limit → upgrade tier or use `--quality low` while iterating
- Timeout → check network; set SDK timeout ≥ 120 s
- Japanese text broken → wrap exactly in quotes; specify font (e.g. `serif Japanese font`)
