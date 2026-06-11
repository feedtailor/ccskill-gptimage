# Virtual Try-On — Changing a person's clothing (identity preservation)

Cookbook 5.2. An editing workflow that **strictly locks the person's identity** while replacing only the clothing.

## When to use

- Virtual try-on features for e-commerce sites
- Visualizing fashion suggestions
- Lookbook generation (many outfits on a single model)
- Costume variations for a character

## Cookbook quote

> "Virtual try-on preserves the person's identity while replacing garments with realistic fabric behavior and integrated lighting. Success requires explicit locks on facial features, body geometry, and pose while allowing only clothing modifications."
> — [Cookbook 5.2](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide)

**Tips**:
- **Enumerate the elements to lock**: face, expression, skin tone, body shape, pose, hair, hairstyle, proportions.
- Limit the replacement scope: `Replace only the clothing`.
- Specify the fit: `fitting the garments naturally to her existing pose and body geometry with realistic fabric behavior`.
- Demand integration: `Match lighting, shadows, and color temperature to the original photo`.
- Eliminate a pasted-on look: `without looking pasted on`.

---

## Prompt example (Cookbook 5.2)

```
Edit the image to dress the woman using the provided clothing images. Do not change her face, facial features, skin tone, body shape, pose, or identity in any way. Preserve her exact likeness, expression, hairstyle, and proportions. Replace only the clothing, fitting the garments naturally to her existing pose and body geometry with realistic fabric behavior. Match lighting, shadows, and color temperature to the original photo so the outfit integrates photorealistically, without looking pasted on. Do not change the background, camera angle, framing, or image quality, and do not add accessories, text, logos, or watermarks.
```

**Parameters**: `size=1024x1536`, `quality=medium`, **5** input images
- Image 1: full-body model photo
- Image 2-5: clothing items (tank top, jacket, boots, etc., individually)

**CLI example**:
```bash
ccskill-gptimage generate \
  "Edit the image to dress the woman using the provided clothing images. Do not change her face ..." \
  --reference ./model.png \
  --reference ./item_tanktop.png \
  --reference ./item_jacket.png \
  --reference ./item_boots.png \
  --quality high
```

> **Note**: The Cookbook original specifies `input_fidelity="high"`, but this **cannot be set** for gpt-image-2 (auto max fidelity). This skill's main validation strips it automatically.

---

## Variation: replace just one garment

```
Edit the image to change only the woman's top to a beige cashmere sweater. Keep her pants, shoes, hair, face, identity, pose, and background exactly as in the reference. The sweater should fit naturally with realistic fabric texture and match the lighting of the scene. Do not add accessories, text, or watermarks.
```

**CLI example**:
```bash
ccskill-gptimage generate \
  "Edit the image to change only the woman's top to a beige cashmere sweater. ..." \
  --reference ./model.png --quality high
```

---

## Variation: specify clothing by text (no garment images)

You can try on outfits with text alone, even without garment images.

```
Edit the image: keep the person's face, identity, body, pose, hair, and background exactly unchanged. Replace only her outfit with a tailored navy double-breasted suit, white dress shirt, and brown leather oxford shoes. Realistic fabric behavior, matching the original photo's lighting and color temperature, not pasted-on. No accessories, no text, no watermarks.
```

---

## Writing Multi-Image Inputs (Cookbook Section 2)

For edits that use multiple images, the official recommendation is to make the **index + role** explicit.

Cookbook Section 2 original:
> "Reference each input by **index and description** ('Image 1: product photo… Image 2: style reference…') and describe how they interact ('apply Image 2's style to Image 1'). When compositing, be explicit about which elements move where."

Applied example:
```
Image 1: the full-body reference photo of the woman.
Images 2-5: individual clothing items (top, jacket, pants, shoes).
Dress the woman in Image 1 with all the clothing shown in Images 2-5.
Preserve the woman's identity, face, body, and pose from Image 1.
```

---

## gpt-image-2-specific notes

- Facial identity is preserved automatically at max fidelity (the Cookbook's `input_fidelity=high` setting is unnecessary for gpt-image-2).
- Beyond 5 input images you approach the **API's context limit** (the Cookbook recommends 5 max).
- More image-input tokens directly raise cost. **Don't pass unnecessary reference images.**
- The edit path re-renders the full canvas, so the **background can change slightly**. If strict preservation is required, use the hybrid approach (crop just the person region with Pillow → edit → paste back).

## Source

- Cookbook 5.2 Virtual Clothing Try-On
- URL: https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide
- Retrieved: 2026-04-23
