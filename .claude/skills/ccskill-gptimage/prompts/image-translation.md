# Image Translation — Multilingual translation of in-image text

Cookbook 4.2. For **localizing existing designs — ads, UI screenshots, packaging, infographics — into another language without rebuilding the layout**.

## When to use

- Localizing marketing assets for international rollout
- Multilingual documents and UI screenshots
- Producing another-language version of an existing infographic

## Cookbook quote

> "Used for localizing existing designs (ads, UI screenshots, packaging, infographics) into another language without rebuilding the layout from scratch."
>
> "The key is to preserve everything except the text—keep typography style, placement, spacing, and hierarchy consistent—while translating verbatim and accurately, with no extra words, no reflow unless necessary, and no unintended edits to logos, icons, or imagery."
> — [Cookbook 4.2](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide)

**Tips**:
- Specifying only the target language is enough. The Cookbook original is very simple.
- Explicitly stating "do not change anything except the text" is important.
- Logos, icons, and photos are preserved by default (even without saying so).

---

## Prompt example (Cookbook 4.2)

```
Translate the text in the infographic to Spanish. Do not change any other aspect of the image.
```

**Parameters**: `size=1024x1536`, `quality=medium`, `images.edit`, 1 input image

**CLI example**:
```bash
$CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py \
  "Translate the text in the infographic to Spanish. Do not change any other aspect of the image." \
  --reference ./infographic_en.png --quality high
```

---

## Variation: English → Japanese

Japanese is a strong area for gpt-image-2. A practical pattern for localizing English-original material into Japanese.

```
Translate all the English text in the image to natural Japanese. Keep the typography style (serif vs sans-serif), sizes, colors, and positions as close to the original as possible. Do not change any logos, icons, photos, colors, or layout. Render Japanese text with appropriate font style that matches the tone of the original (e.g., serif English → Mincho-like Japanese serif; sans-serif English → Gothic-like Japanese sans-serif).
```

**CLI example**:
```bash
$CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py \
  "Translate all the English text in the image to natural Japanese. Keep the typography style ..." \
  --reference ./pitch_deck_en.png --quality high
```

---

## Variation: keeping specific proper nouns untranslated

```
Translate the body text to Japanese, but keep the product name "MailGuard" and the company name "feedtailor" in the original English spelling. Do not change layout, colors, or imagery.
```

---

## Caveats and limits

- **Cookbook states**: "with no extra words, no reflow unless necessary, and no unintended edits to logos, icons, or imagery" — when the translated text gets longer, it may reflow on its own.
- Translation into Japanese does **not auto-detect vertical vs. horizontal writing**. If needed, specify it in the prompt (`keep horizontal text layout` or `convert to vertical Japanese text layout`).
- When the image contains small body text, `quality=high` is recommended (low quality breaks Japanese glyphs).
- Because this goes through the edit path, the **full canvas is re-rendered**. Logos and icons are strongly preserved by gpt-image-2's auto max fidelity, but **pixel-identical preservation is not guaranteed**.

## gpt-image-2-specific notes

- **No need to specify `input_fidelity`** (auto max). It isn't documented in the Cookbook but is always in effect for gpt-image-2.
- When translating multiple pages, **editing one image at a time** is more stable (a single API call handles one image).
- When the translated text length changes significantly (EN→JA tends to shorten, JA→EN tends to lengthen), either **accept the layout shift or instruct the model to paraphrase that text more concisely**.

## Source

- Cookbook 4.2 Translation in Images
- URL: https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide
- Retrieved: 2026-04-23
