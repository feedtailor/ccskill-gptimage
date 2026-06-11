# Ads & Marketing (including in-image text)

Combines Cookbook 4.6 (Ads Generation) + 5.5 (Marketing Creatives with Real Text In-Image). The shared principle is to **include the brand + audience + copy explicitly in the prompt**.

## When to use

- Ad creatives (Instagram, magazines, transit ads)
- Billboard / signage mockups
- Social media assets with campaign copy laid over a product image
- Campaign teaser visuals

## Cookbook principles

### 4.6 — Write it as a brief

> Write ads as a **creative brief**, not a technical spec. Describe the brand, audience, concept, composition, and exact copy, and leave the creative judgment to the model.

### 5.5 — Make text render verbatim

> "When baking marketing copy into an image, lock typography with explicit constraints: quote the exact copy, demand verbatim rendering with no extra characters, and describe placement and font style."

**Tips**:
- Use **the strongest possible binding**, like `Billboard text (EXACT, verbatim, no extra characters):`
- Always specify typography: `bold sans-serif, high contrast, centered, clean kerning`
- Add `Ensure text appears once and is perfectly legible.` to prevent duplicate rendering
- Use `No watermarks, no logos.` to exclude stray marks

---

## Prompt example 1: Brand campaign image (Cookbook 4.6)

```
Give me a cool in culture ad / fashion shot for a brand called Thread.
It's a hip young street brand. The ad shows a group of friends hanging out together with the tagline "Yours to Create."
Make it feel like a polished campaign image for a youth streetwear audience: stylish, contemporary, energetic, and tasteful.
Use clean composition, strong color direction, natural poses, and premium fashion photography cues.
Render the tagline exactly once, clearly and legibly, integrated into the ad layout.
No extra text, no watermarks, no unrelated logos.
```

**Parameters**: `size=1024x1536`, `quality=medium`

**CLI example**:
```bash
$CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py \
  "Give me a cool in culture ad / fashion shot for a brand called Thread. ..." \
  --size 1024x1536 --quality high \
  --output-name thread_campaign_01
```

---

## Prompt example 2: A billboard with copy laid over an existing product image (Cookbook 5.5 / edit path)

```
Create a realistic billboard mockup of the shampoo on a highway scene during sunset.
Billboard text (EXACT, verbatim, no extra characters):
"Fresh and clean"
Typography: bold sans-serif, high contrast, centered, clean kerning.
Ensure text appears once and is perfectly legible.
No watermarks, no logos.
```

**Parameters**: `size=1024x1536`, `quality=medium`, 1 input image (shampoo bottle)

**CLI example**:
```bash
$CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py \
  "Create a realistic billboard mockup of the shampoo on a highway scene during sunset. Billboard text (EXACT, verbatim, no extra characters): \"Fresh and clean\" Typography: bold sans-serif, high contrast, centered, clean kerning. Ensure text appears once and is perfectly legible. No watermarks, no logos." \
  --reference ./product_bottle.png --quality high
```

---

## Ads with Japanese copy (leveraging gpt-image-2's strength)

gpt-image-2 renders Japanese text with high accuracy, so you can produce ads with Japanese copy like the following in one shot.

```
Create a subway poster mockup for a Japanese matcha drink brand launching spring 2026.
Ad copy (EXACT, verbatim, in Japanese):
"一杯で、春。"
and subtitle:
"新緑シーズン限定ブレンド"
Typography: large bold Japanese serif (like Mincho) for the main copy, medium-weight Japanese sans-serif (like Gothic) for the subtitle.
Green-and-white palette, minimal layout, a single matcha drink centered.
No watermarks, no extra text, no logos.
```

**Key points**:
- Specify Japanese fonts explicitly (`Mincho` / `Gothic`)
- Wrap the copy in quotes — `"一杯で、春。"` — for verbatim rendering
- Include punctuation inside the quotes (so even the period `。` is reproduced exactly)

> **Related**: when using **Japanese signage or cultural icons** in streetscape, interior, or local-flavor visuals, also see [`cultural-atmosphere.md`](cultural-atmosphere.md). It covers the pitfall of forcing "illegible characters only" and erasing the culture, along with patterns to avoid it.

---

## gpt-image-2-specific notes

- To avoid the **duplicate-text rendering bug**, always include `Ensure text appears once`
- Long copy is prone to rendering errors. **Catchphrases of about 10–15 characters** are the practical limit
- When bringing in a product image via the edit path, **the product's shape and logo are preserved automatically** (no `input_fidelity` needed)
- If cost is the priority, try with `quality=low` and deliver at `quality=high` (`medium` is a halfway point where text gets blurry)

## Source

- Cookbook 4.6 Ads Generation / 5.5 Marketing Creatives with Real Text In-Image
- URL: https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide
- Retrieved: 2026-04-23
