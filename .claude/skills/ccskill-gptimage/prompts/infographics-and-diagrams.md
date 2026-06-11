# Infographics / Diagrams / Slides & Charts

Combines Cookbook 4.1, 4.9, and 4.10. The shared trait is **dense layout and heavy in-image text**, a category where `quality=high` is recommended.

## When to use

- Technical flow diagrams (explaining a mechanism with both visuals and text)
- Conceptual diagrams for science/education (learning material)
- Business slides (pitch decks, dashboards, KPI panels)
- Data visualization (TAM/SAM/SOM, bar charts, timelines)

## Core principles (Cookbook quotes)

> "Use infographics to explain structured information for a specific audience: students, executives, customers, or the general public."
> "For dense layouts or heavy in-image text, it's recommended to set output generation quality to 'high'."
> — [Cookbook 4.1](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide)

**Key tips**:
- Include the target audience (students/executives/general public/children) at the start of the prompt
- Write specific data values (e.g. `TAM: $42B`) **directly into the prompt** — letting the model invent the numbers makes them drift
- State the decorations you want excluded in Constraints (e.g. `Avoid clip art, stock photography, gradients, shadows, decorative elements`)

---

## Prompt example 1: Technical infographic explaining how a machine works (Cookbook 4.1)

```
Create a detailed Infographic of the functioning and flow of an automatic coffee machine like a Jura.
From bean basket, to grinding, to scale, water tank, boiler, etc.
I'd like to understand technically and visually the flow.
```

**Parameters**: `size=1024x1536`, `quality=medium` (use `high` if the layout is dense)

**CLI example**:
```bash
$CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py \
  "Create a detailed Infographic of the functioning and flow of an automatic coffee machine like a Jura. From bean basket, to grinding, to scale, water tank, boiler, etc. I'd like to understand technically and visually the flow." \
  --size 1024x1536 --quality high
```

---

## Prompt example 2: Scientific diagram for learning (Cookbook 4.9)

```
Create a simple biology diagram titled "Cellular Respiration at a Glance" for high school students.

Show how glucose turns into energy inside a cell. Include glycolysis, the Krebs cycle, and the electron transport chain.
Use arrows to connect the steps, and label the main molecules: glucose, pyruvate, ATP, NADH, FADH2, CO2, O2, and H2O.
Make it look like a clean classroom handout or slide, with a white background, simple icons, clear labels, and easy-to-read text.

Avoid tiny text, extra decoration, or anything that makes the diagram hard to understand.
```

**Parameters**: `size=1536x1024`, `quality=high` (required because of the dense small labels)

---

## Prompt example 3: A single pitch-deck slide (Cookbook 4.10)

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

**Parameters**: `size=1536x864`, `quality=high`

> **Note**: `1536x864` is not in the current `SIZE_CHOICES` of `generate_image.py`. The closest alternative is `1536x1024` (16:10). If you need to match the Cookbook exactly, consider expanding the choices in a separate issue.

---

## Infographics containing Japanese text

gpt-image-2 is strong at rendering Japanese kanji and kana — the same lineage as the `14_tategaki` example shown in SKILL.

```
Create a clean bilingual infographic titled "DMARC の仕組み" for a Japanese SaaS audience.
Layout the flow left-to-right: 送信者 (Sender) → DNS TXT レコード → 受信サーバー → 認証結果 (Pass / Fail / Quarantine).
Label each step in both Japanese and English, Japanese as the primary label in bold serif font.
White background, navy and teal accent colors, no decorative illustrations.
Avoid watermarks, logos, or stock imagery.
```

---

## gpt-image-2-specific notes

- **A situation where `quality=high` is worth the cost.** With dense text, `medium` tends to collapse
- Portrait (`1024x1536`) at `high` is $0.165, cheaper than square `high` — portrait-oriented infographics are actually a better deal in portrait
- Always write a Constraints section (patterns like `Avoid clip art, stock photography, gradients, ...` are officially recommended)

## Source

- Cookbook 4.1 Infographics / 4.9 Scientific-Educational / 4.10 Slides Diagrams Charts
- URL: https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide
- Retrieved: 2026-04-23
