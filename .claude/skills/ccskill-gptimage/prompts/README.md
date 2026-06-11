# prompts/ — Use-case prompt collection

This directory organizes the 23 use cases from the OpenAI Cookbook [GPT Image Generation Models Prompting Guide](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide) into **14 files consolidated by related use case**.

## Usage (for Claude)

Once you have identified the rough use case in `SKILL.md`, Read the relevant file to pull in the **finished prompt template + parameters + gpt-image-2-specific notes**, and compose it to match the user's intent.

Each file is meant to be **loaded only when needed** on a progressive-disclosure basis, so there is no need to memorize all of them.

## Index

### Generation (text → image)

| File | Use cases covered | Cookbook section |
|---|---|---|
| [infographics-and-diagrams.md](infographics-and-diagrams.md) | Infographics / concept diagrams / science & education diagrams / slides & charts | 4.1, 4.9, 4.10 |
| [photorealism.md](photorealism.md) | Natural photographic rendering / scenes with historical context | 4.3, 4.4 |
| [logo.md](logo.md) | Brand logos / variant generation (`n`) | 4.5 |
| [ads-and-marketing.md](ads-and-marketing.md) | Ad visuals / exact-match text in images | 4.6, 5.5 |
| [comic-and-storyboard.md](comic-and-storyboard.md) | Comics / panel layout / storyboards | 4.7 |
| [ui-mockups.md](ui-mockups.md) | Mobile/Web app UI mockups | 4.8 |
| [character-and-concept.md](character-and-concept.md) | Character consistency / holiday cards / toy packaging | 6.2, 6.3, 6.4 |
| [cultural-atmosphere.md](cultural-atmosphere.md) | Cultural atmosphere (Japanese signage and streetscapes) | Sec.2 + verified (#015) |

### Editing (text + image → image)

| File | Use cases covered | Cookbook section |
|---|---|---|
| [image-translation.md](image-translation.md) | Multilingual translation of in-image text | 4.2 |
| [style-transfer.md](style-transfer.md) | Apply a reference image's style to different content | 5.1 |
| [try-on.md](try-on.md) | Change a person's clothing (identity preserved) | 5.2 |
| [sketch-to-render.md](sketch-to-render.md) | Hand-drawn sketch → photorealistic | 5.3 |
| [product-mockup.md](product-mockup.md) | Product extraction & background removal / precise interior replacement | 5.4, 6.1 |
| [scene-transform.md](scene-transform.md) | Weather & time-of-day change / object removal | 5.6, 5.7 |
| [scene-composite.md](scene-composite.md) | Person into a new scene / multi-image compositing | 5.8, 5.9 |

## Notes common to all files

1. **These prompt guides are written in English**: prose is in English, and the prompt examples are in English as they are sent to the model (source: Cookbook + retrieved 2026-04-23).
2. **`input_fidelity=high` may appear in the Cookbook**, but with gpt-image-2 it **cannot be specified (400 error)** due to automatic maximum fidelity. This skill strips it automatically in the main validation of `generate_image.py`, but do not add it explicitly when composing prompts.
3. **`background: transparent` is unsupported by gpt-image-2**. If you need transparency, (a) switch to `--model gpt-image-1.5`, (b) post-process with rembg, or (c) switch to `ccskill-nanobanana`.
4. **Cost gotcha**: `1024×1536` (portrait) at `high` is **$0.165**, cheaper than `1024×1024` at `high` ($0.211).
5. The edit path (specifying `--reference`) is **always a full-canvas redraw** (the mask is guidance only, as the official Cookbook states). If pixel-level preservation is required, use a Pillow-style hybrid of crop → edit → paste back.

## Source

All prompt examples are quoted from the OpenAI Cookbook "GPT Image Generation Models Prompting Guide." The source URL is noted directly below the relevant prompt in each file.
