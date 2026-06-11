# Sketch → Photorealistic Render

Cookbook 5.3. Convert a rough sketch into photographic realism. **Preserve layout, perspective, and proportions** while making only the materials and light photorealistic.

## When to use

- Concept validation of design sketches (concept → photo-like)
- Photorealizing hand-drawn architecture/interior roughs
- Storyboard → live-action visualization
- A fun use case: turning a child's drawing into a photo

## Cookbook quote

> "Convert rough sketches into photorealistic images while preserving layout and perspective. Add realism through materials and lighting without introducing new elements."
> — [Cookbook 5.3](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide)

**Tips**:
- Explicitly write **Preserve the exact layout, proportions, and perspective**.
- Give freedom to specify materials and lighting.
- **Forbid adding new elements**: `Do not add new elements or text.`

---

## Prompt example (Cookbook 5.3)

```
Turn this drawing into a photorealistic image.
Preserve the exact layout, proportions, and perspective.
Choose realistic materials and lighting consistent with the sketch intent.
Do not add new elements or text.
```

**Parameters**: `size=1024x1536`, `quality=medium`, 1 input image (sketch)

**CLI example**:
```bash
$CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py \
  "Turn this drawing into a photorealistic image. Preserve the exact layout, proportions, and perspective. Choose realistic materials and lighting consistent with the sketch intent. Do not add new elements or text." \
  --reference ./sketch.png --quality high
```

---

## Variation: hint at materials, light, and setting

When you want to convey the sketch's intent more concretely:

```
Turn this architectural sketch into a photorealistic rendering.
Preserve the exact layout, proportions, camera angle, and perspective from the sketch.
Add realism:
- Materials: warm oak floorboards, white matte walls, brushed brass fittings, natural linen curtains
- Lighting: soft afternoon daylight from the left window, with subtle warm ambient fill
- Atmosphere: slight dust particles in the sunbeam, shallow depth of field
Do not add new furniture, people, or text that is not in the sketch.
```

---

## Variation: child's drawing → photorealistic

An entertainment use case (e.g., a family gift). Not in the original Cookbook, but a fun use specific to this skill.

```
Turn this child's drawing of an imaginary creature into a photorealistic creature portrait.
Preserve the exact pose, body proportions, relative size of features, and color palette from the drawing — even if anatomically unusual.
Render as if it were a real animal photographed in natural habitat: realistic fur or scales texture, natural lighting, soft bokeh background.
Do not simplify or correct the creature's design; keep the original's spirit.
No text, no watermarks.
```

---

## gpt-image-2-specific notes

- Thanks to **auto max fidelity**, the "sketch's composition and lines" are strongly preserved (`input_fidelity` not needed, and would error).
- As always with the edit path, however, the **full canvas is re-rendered**, so fine lines won't match one-to-one.
- A **faint/messy** sketch leaves more interpretive room for photorealization. The higher a sketch's brightness and contrast, the better it is preserved.
- The model can add new elements on its own, so always include `Do not add new elements or text.`
- `quality=high` helps reproduce the feel of materials.

## Source

- Cookbook 5.3 Drawing → Image (Rendering)
- URL: https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide
- Retrieved: 2026-04-23
