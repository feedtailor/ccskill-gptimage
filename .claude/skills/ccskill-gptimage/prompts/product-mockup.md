# Product Mockup / Interior Swap — Precise replacement of the target only

Combines Cookbook 5.4 (Product Mockups) and 6.1 (Interior design "swap"). The shared design is **"cleanly extract or replace only what should be there, fully preserve the surroundings."**

## When to use

- Catalog images for e-commerce (cut out the product onto a white background)
- Asset cleanup for design specs and design systems
- Swapping just the furniture in an interior photo for a different model
- Placement variations of product packaging

## Cookbook quote

### Product extraction (5.4)

> "Product extraction and background removal for catalogs and design systems, emphasizing edge quality and label preservation while maintaining opaque backgrounds."

### Precise replacement of interior objects (6.1)

> "Surgical object replacement in real architectural photography while preserving lighting, shadows, camera angle, and surrounding context for photorealistic results."
> — [Cookbook 5.4 / 6.1](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide)

**Shared tips**:
- Name the target concretely (`the product` / `replace ONLY the white chairs`)
- Demand edge quality: `crisp silhouette, no halos/fringing`
- Preserve label/text legibility: `Preserve product geometry and label legibility exactly`
- Preserve list for the surroundings: `Preserve camera angle, room lighting, floor shadows, and surrounding objects`
- Forbid restyling: `Do not restyle the product; only remove background and lightly polish.`

---

## Prompt example 1: Product extraction (Cookbook 5.4)

```
Extract the product from the input image and place it on a plain white opaque background.
Output: centered product, crisp silhouette, no halos/fringing.
Preserve product geometry and label legibility exactly.
Add only light polishing and a subtle realistic contact shadow.
Do not restyle the product; only remove background and lightly polish.
```

**Parameters**: `size=1024x1536`, `quality=medium`, 1 input image, **`--background opaque`**

**CLI example**:
```bash
ccskill-gptimage generate \
  "Extract the product from the input image and place it on a plain white opaque background. ..." \
  --reference ./product_raw.jpg \
  --background opaque --quality high
```

### When you need a transparent PNG

gpt-image-2 does not support transparent. If you want the product as a transparent PNG:

1. **Extract on a white background → remove background with rembg** (recommended — leverages gpt-image-2's edge quality):
   ```bash
   ccskill-gptimage generate \
     "Extract the product..." --reference ./product_raw.jpg \
     --output-name product_white_bg
   rembg i generated_images/product_white_bg.png generated_images/product_alpha.png
   ```
2. Switch to `--model gpt-image-1.5 --background transparent` (legacy model)
3. Switch to `ccskill-nanobanana`

---

## Prompt example 2: Precise replacement of interior furniture (Cookbook 6.1)

```
In this room photo, replace ONLY white with chairs made of wood.
Preserve camera angle, room lighting, floor shadows, and surrounding objects.
Keep all other aspects of the image unchanged.
Photorealistic contact shadows and fabric texture.
```

**Parameters**: `size=1536x1024`, `quality=medium`, 1 input image

**CLI example**:
```bash
ccskill-gptimage generate \
  "In this room photo, replace ONLY the white chairs with chairs made of warm oak wood with natural grain. Preserve camera angle, room lighting, floor shadows, and surrounding objects. Keep all other aspects of the image unchanged. Photorealistic contact shadows and wood texture." \
  --reference ./living_room.jpg \
  --size 1536x1024 --quality high
```

---

## Advanced: Place the product into a different scene

A pattern that places a studio white-background product into a **lifestyle scene**.

```
Place the product from the reference image on a warm oak dining table, next to a cup of black coffee and a linen napkin, in a modern Scandinavian kitchen with soft morning light from a window on the left.
Preserve the product's exact shape, label, color, and proportions from the reference.
Do not change the product in any way — only integrate it into the new scene with realistic lighting and contact shadows.
No watermarks, no extra text.
```

---

## gpt-image-2-specific notes

- Always write **Preserve product geometry and label legibility exactly**. Without it, label text gets rewritten by the model's invention
- With **automatic maximum fidelity**, product shape is strongly preserved (`input_fidelity` need not — and must not — be specified)
- For product extraction, use `--background opaque` and make it transparent in post as needed for cleaner results
- For local edits like the furniture swap in 6.1, operate with an understanding of the edit API's **full-canvas redraw** behavior. If strict preservation is required, use a Pillow hybrid (see the "Local editing" section of SKILL.md)
- For interiors, **1536x1024 (landscape)** is natural

## Source

- Cookbook 5.4 Product Mockups / 6.1 Interior design "swap"
- URL: https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide
- Retrieved: 2026-04-23
