# Cultural Atmosphere — conveying a culture's distinctive feel (Japanese signage and streetscapes)

To give an image a sense of "belonging to a particular country," the key is how you handle **culture-specific text elements (signs, signage, shop names)** and the **linguistic icons of the streetscape**. This guide systematizes, as a reusable pattern, the verified insights gained from rewriting **19_urban_tokyo_rainy_night** from v2 to v3 during the issue #015 Phase 4 effectiveness study.

## When to use

- Streetscape scenes (the Shibuya/Shinjuku entertainment districts, Asian night markets, European old towns, etc.)
- When you want a "local feel" in ads / marketing visuals (use alongside `prompts/ads-and-marketing.md`)
- In-store mockups / shopping arcades / back-alley everyday atmosphere
- Tourism and inbound-travel content

## Core principle — don't force "unreadable text"

The biggest pitfall that erases cultural atmosphere is **overusing negative Constraints**. When you try to avoid real brands by forcing "unreadable text only," you also lose the iconic quality of the culture.

---

## Section A: leverage a culture's text elements

### A-1. The negative-Constraints trap (v2 → v3, verified)

The diff that clearly produced results in the 19_urban_tokyo_rainy_night rewrite:

| | How Constraints were written | Result |
|---|---|---|
| ❌ v2 (weakened) | `no readable specific text on signs (kanji shapes only)` | Forcing "unreadable kanji shapes only" stripped away even the Japanese feel of the shop signs, producing a **flat, placeless cityscape with no sense of where it is** |
| ✅ v3 (improved) | `Japanese characters on signs should be plausible Japanese language (not English alphabet, not gibberish)` + `use generic / fictional shop names, not real brand names` | **The Shibuya scramble crossing was reproduced as if real.** A row of natural Japanese signs lined up |

Examples of signs actually rendered in v3 (fictional but natural as Japanese):

> `カラオケ 747` / `居酒屋 2F・3F` / `薬方 くすり・化粧品` / `牛繁 焼肉` / `コンタクトのアイシティ`

**Verified image**: [`assets/capability-survey/categories/19_urban_tokyo_rainy_night_v3.png`](../../../../assets/capability-survey/categories/19_urban_tokyo_rainy_night_v3.png)

**Lesson**: Writing `no readable text` out of a desire to "avoid real names" kills the culture. The correct move is to **specify "readable, fictional language" in the affirmative**.

### A-2. Enumerate sign types concretely in Key details

Rather than just "there are Japanese signs," enumerating **what kinds of signs** increases density and authenticity:

```
tategaki kanji shop signs in deep crimson, electric cyan and warm gold
karaoke / izakaya signs in stacked Japanese characters
small ramen-shop lanterns glowing on side streets
vertical neon signs stacked along narrow alleys
```

- Explicitly specifying **vertical writing (tategaki)** instantly conveys "Japaneseness"
- Specifying colors (`deep crimson, electric cyan, warm gold`) too stabilizes the texture of a nighttime entertainment district
- Mix in one or two **everyday icons** such as lanterns, noren curtains, or vending machines

---

## Section B: the trade-off between "avoiding real brands" and "cultural authenticity"

- gpt-image-2 is **good at inventing fictional Japanese brand names**. Even just `use generic / fictional shop names` mass-produces natural signage
- However, **names close to real ones occasionally slip in**, like `龍角散` (because the model holds them as knowledge)
- If you need **complete fictionality**, additionally state the following:
  ```
  Do not use any real brand names that exist in Japan today. All shop names must be invented.
  ```
- But this is a **trade-off** — the tighter the constraint, the more "authentic feel" is shaved off. Choose based on your project's requirements:

| Requirement | Recommendation |
|---|---|
| Authenticity-first for ads, landing pages, etc. (some real-looking names acceptable) | `use generic / fictional shop names` only. Keep it loose |
| Legally/rights-wise, not a single real brand may appear | The above + append `Do not use any real brand names ... All shop names must be invented.` Visually check the output |

> **Important**: When complete fictionality is a requirement, **always visually check after generation**. Real names can slip in even when constrained by the prompt, so the ultimate safeguard is human review.

---

## gpt-image-2-specific notes

- Sign clusters with lots of text are prone to rendering errors. **Render 1–2 hero signs literally, and treat the background sign cluster as "atmosphere."**
- The linguistic authenticity of signage clearly improves at `quality=high` (at `medium`, text tends to break down into gibberish)
- The risk of real brands slipping in **cannot be reduced to zero by the prompt alone** — if complete fictionality is a requirement, visual review is mandatory (Section B)
- Related principles: for affirmative empty-state declarations, see "Empty / null state declaration" in [`photorealism.md`](photorealism.md); for literal copy rendering, see [`ads-and-marketing.md`](ads-and-marketing.md)

## Source

- Verified from: issue #015 Phase 4 effectiveness study (v2 → v3 rewrite of 19_urban_tokyo_rainy_night, 2026-04-24)
- Cookbook Section 2 "Text in Images" / "Constraints": https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide
- Retrieved: 2026-04-23 (Cookbook) / 2026-04-24 (verification)
