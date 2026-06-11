# Comic / Storyboard

Cookbook 4.7. Turn a story into a **multi-panel** visual narrative. Describe each panel as an independent visual beat — concrete and action-focused.

## When to use

- 4-panel comics / strips for vertical social reels
- Storyboards for video content
- Step-by-step product walkthroughs (Step 1/2/3...)
- Illustration series for novels and essays

## Cookbook quote

> "Story-to-comic-strip workflows benefit from defining each beat as concrete, action-focused descriptions. Maintains readability and pacing across panels."
> — [Cookbook 4.7](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide)

**Tips**:
- **State panel numbers explicitly** (`Panel 1:`, `Panel 2:`, …)
- Use concrete verbs to describe "what is happening" in each panel
- **Repeat the character's appearance, clothing, and gaze in every panel** (prevents drift; Cookbook Section 2 "Iterate" principle)
- Explicitly state that it's the "same character" (`The same pet`, `The same protagonist`)

---

## Prompt example (Cookbook 4.7)

```
Create a short vertical comic-style reel with 4 equal-sized panels.
Panel 1: The owner leaves through the front door. The pet is framed in the window behind them, small against the glass, eyes wide, paws pressed high, the house suddenly quiet.
Panel 2: The door clicks shut. Silence breaks. The pet slowly turns toward the empty house, posture shifting, eyes sharp with possibility.
Panel 3: The house transformed. The pet sprawls across the couch like it owns the place, crumbs nearby, sunlight cutting across the room like a spotlight.
Panel 4: The door opens. The pet is seated perfectly by the entrance, alert and composed, as if nothing happened.
```

**Parameters**: `size=1024x1536` (portrait, compatible with social reels), `quality=medium`

**CLI example**:
```bash
ccskill-gptimage generate \
  "Create a short vertical comic-style reel with 4 equal-sized panels. Panel 1: ..." \
  --size 1024x1536 --quality high \
  --output-name petstory_reel
```

---

## Variation: 3-step product walkthrough

```
Create a horizontal 3-panel infographic illustrating how to use the product.
Panel 1: A woman opens the box, smiling with anticipation. Clean white studio background.
Panel 2: Same woman is fitting the device on her wrist, focused and pleased.
Panel 3: Same woman is walking outdoors, wearing the device visibly on her wrist, with morning sunlight.
Character Consistency: Same woman, same hair, same skin tone, same face across all panels.
Flat modern illustration style, soft pastel colors, minimal decoration.
No text on panels. No watermarks.
```

**Parameters**: `size=1536x1024` (landscape), `quality=high`

**Note**: Use a `Character Consistency:` block to explicitly state that it's the **same person**. Combine with the Cookbook 6.4 (character consistency) technique.

---

## Japanese manga style (with vertical speech bubbles)

gpt-image-2 is strong at rendering Japanese text, so you can produce manga with dialogue too.

```
Create a 4-panel Japanese manga-style short story, arranged top-to-bottom.
Panel 1: A tired salaryman on the last train, staring out the window. Speech bubble (exact Japanese, vertical right-to-left text): "もう終電か..."
Panel 2: His phone vibrates. Text message balloon: "今日もおつかれ！"
Panel 3: He smiles slightly, looking at the phone.
Panel 4: He closes his eyes, the train rocking gently.
Style: clean black-and-white manga inking, screentone shading, standard manga panel borders.
Keep the same salaryman character across all panels. No watermarks.
```

> **Note**: Vertical text and right-to-left panel order are not always reproduced. If strict reading order matters, plan to **reorder the panels by hand after generation**.

---

## gpt-image-2-specific notes

- **4 panels is the stable count.** Beyond 6, each panel's rendering degrades (the aspect ratio gets squeezed).
- **Appearance drift** of the same character happens easily. The official Cookbook 4.7 recommendation is to "**rewrite the character's appearance in every panel**".
- Portrait (`1024x1536`) fits TikTok/Reels sizes; landscape (`1536x1024`) suits slides and horizontal scrolling.
- Cost: a single poster containing 4 panels is generated as one image, so even `high` is a single charge ($0.165–$0.211).

## Source

- Cookbook 4.7 Story-to-Comic Strip
- URL: https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide
- Retrieved: 2026-04-23
