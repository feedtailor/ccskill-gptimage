# Style Transfer — Carry a reference image's visual language to new content

Cookbook 5.1. Keep the **palette, texture, and brushwork** of a reference image while swapping the subject or scene.

## When to use

- Unifying artwork style across a series
- Generating additional assets that follow a brand visual guide
- Reusing the "mood" of a reference work to make an illustration with a different composition

## Cookbook quote

> "Preserves the visual language (palette, texture, brushwork) from a reference image while changing the subject or scene. Success requires specifying what stays consistent and what changes, with hard constraints to prevent drift."
> — [Cookbook 5.1](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide)

**Tips**:
- Separate and state explicitly the "style elements to preserve" and the "content to change".
- Verbalize the style to preserve: `palette, texture, brushwork, film grain, line thickness`.
- **Repeat the preserve constraints on every iteration** (to prevent drift).

---

## Prompt example (Cookbook 5.1)

```
Use the same style from the input image and generate a man riding a motorcycle on a white background.
```

**Parameters**: `size=1024x1536`, `quality=medium`, 1 input image (style reference)

**CLI example**:
```bash
$CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py \
  "Use the same style from the input image and generate a man riding a motorcycle on a white background." \
  --reference ./style_reference.png --quality high
```

---

## Variation: spell out style elements for a stronger reflection

The Cookbook original is simple, but making the style elements concrete reduces drift.

```
Use the same visual style as the input image — specifically:
- the muted watercolor palette (dusty pinks, soft grays, pale blues)
- visible paper texture and subtle grain
- soft, slightly feathered line work
- painterly brush strokes rather than sharp edges
Apply this style to a new subject: a young woman sitting at a cafe window in the rain, looking out, cup of coffee in hand.
Preserve the exact style properties listed above. Do not shift to photorealism.
```

**CLI example**:
```bash
$CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py \
  "Use the same visual style as the input image — specifically: ..." \
  --reference ./watercolor_ref.png --quality high
```

---

## Pattern for building a series

Treat the first image as an **anchor**; when you want to build out a series, combine this with the Anchor-first technique in character-and-concept.md.

```
Use the same style and color palette as the input image.
Generate the next scene in the series: [describe the scene].
Style Consistency:
- Same line weight, color saturation, and texture as the reference
- Same illustration technique (do not shift to digital painting or photorealism)
Constraints:
- No text, no watermarks
- Match the reference's aspect ratio
```

---

## gpt-image-2-specific notes

- **Auto max fidelity** also picks up the input image's style strongly (`input_fidelity` not needed).
- To blend multiple style references, you can pass **two or more `--reference`** images (Multi-Image Inputs pattern).
- Style transfer is **not a perfect copy**. Treat it as "inheriting the mood".
- For **medium conversion** like photo→illustration or illustration→photo, the sketch-to-render.md pattern is more appropriate than style transfer.

## Source

- Cookbook 5.1 Style Transfer
- URL: https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide
- Retrieved: 2026-04-23
