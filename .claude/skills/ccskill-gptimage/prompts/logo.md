# Logo

Cookbook 4.5. Brand logo generation, where the officially recommended workflow is to **generate variations in parallel with `n=4`** and pick from them.

## When to use

- Logo concepts for a new brand or service
- Refresh candidates for an existing brand
- Icons, marks, symbol marks

## Cookbook quotes

> "Strong logo generation comes from clear brand constraints and simplicity. Describe the brand's personality and use case, then ask for a clean, original mark with strong shape, balanced negative space, and scalability across sizes."
> "You can specify parameter 'n' to denote the number of variations you would like to generate."
> — [Cookbook 4.5](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide)

**Design principles**:
- The brand's personality (warm, timeless, minimal, technical, playful…) in words
- The use context (local bakery, SaaS product, tech startup…)
- The nature of the shape (vector-like shapes, strong silhouette, balanced negative space)
- Scalability requirement (`reads clearly at small and large sizes`)
- Forbidden elements (gradients, watermarks, copyright infringement)

---

## Prompt example (Cookbook 4.5)

```
Create an original, non-infringing logo for a company called Field & Flour, a local bakery.
The logo should feel warm, simple, and timeless. Use clean, vector-like shapes, a strong silhouette, and balanced negative space.
Favor simplicity over detail so it reads clearly at small and large sizes. Flat design, minimal strokes, no gradients unless essential.
Plain background. Deliver a single centered logo with generous padding. No watermark.
```

**Parameters**: `size=1024x1536`, `quality=medium`, **`n=4`** (generate 4 variations in parallel)

---

## CLI example

**Note**: the current `generate_image.py` hardcodes `n=1`, so there's no way to specify `n=4` directly. The practical approach is to **call it 4 times**:

```bash
for i in 1 2 3 4; do
  $CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py \
    "Create an original, non-infringing logo for a company called Field & Flour, a local bakery. The logo should feel warm, simple, and timeless. Use clean, vector-like shapes, a strong silhouette, and balanced negative space. Favor simplicity over detail so it reads clearly at small and large sizes. Flat design, minimal strokes, no gradients unless essential. Plain background. Deliver a single centered logo with generous padding. No watermark." \
    --size 1024x1024 --quality high \
    --output-name "logo_fieldflour_v${i}"
done
```

Adding a `--n` option in the future is left for a separate issue.

---

## When you need a transparent PNG

gpt-image-2 **does not accept `background: transparent`** (400 error). If a logo use case needs transparency, pick one of:

1. **rembg post-processing (recommended)** — generate a plain-background logo with gpt-image-2, then remove the background:
   ```bash
   $CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py \
     "...logo prompt... plain white background..." --output-name logo_raw
   rembg i generated_images/logo_raw.png generated_images/logo_alpha.png
   ```

2. **Switch to `gpt-image-1.5`** (the older model that supports transparency):
   ```bash
   $CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py \
     "minimalist fox logo, flat vector, navy and gold" \
     --model gpt-image-1.5 --background transparent --output-format png
   ```

3. **Switch to `ccskill-nanobanana`** (sister skill)

## gpt-image-2-specific notes

- Square (`1024x1024`) is natural for a logo, but **using portrait `1024x1536` generates more cheaply**, padding included (a cost gotcha)
- The Cookbook recommends `n=4`, but a **workflow of generating 4 times with the same prompt** is a viable substitute
- When you want to line up variations for comparison, distinguishing filenames with `--output-name` is important
- Official phrases to avoid copyright risk: `original, non-infringing` / `No watermark`

## Source

- Cookbook 4.5 Logo Generation
- URL: https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide
- Retrieved: 2026-04-23
