# Character Consistency / Concept Art / Keepsake

Combines Cookbook 6.2 (3D Pop-Up Holiday Card), 6.3 (Collectible Action Figure), and 6.4 (Children's Book Art with Character Consistency). The shared themes are **conveying a premium material feel** and **maintaining a character's identity across multiple images**.

## When to use

- Picture books / multi-scene illustration series (the same character appears in multiple scenes)
- **Concept images** for toys and collectibles (for advertising physical products)
- Seasonal greeting cards (New Year cards, Christmas cards)
- Scene variations for corporate mascots and brand characters

## Core principles

### Premium material feel (6.2, 6.3)

> "Premium concept artwork benefits from describing it like product photography: tactile materials (paper layers, textures, worn fur, plastic edges), soft studio lighting, shallow depth of field. The result should feel like a photo of a physical keepsake or retail product, not an illustration."
> — [Cookbook 6.2 / 6.3](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide)

### Character consistency (6.4)

> "Multi-scene character workflows require an 'anchor image' first, then edit-based continuations that explicitly repeat the character's outfit, facial features, and style. Restate 'do not redesign the character' in every follow-up."

**Three design pillars**:
- **Split into 4 blocks: Scene / Mood / Style / Constraints** (the standard 6.2 / 6.3 format)
- **Anchor-first approach** (6.4): lock the design in one image first → derive the rest via edits
- **Material-feel vocabulary**: `tactile`, `worn`, `stitched`, `realistic plastic`, `painted metal`, `bokeh`

---

## Prompt example 1: holiday card (Cookbook 6.2)

```
Create a Christmas holiday card illustration.

Scene:
a cozy Christmas scene with an old teddy bear sitting inside a keepsake box,
slightly worn fur, soft stitching repairs, placed near a window with falling snow outside.
The scene suggests the child has grown up, but the memories remain.

Mood:
Warm, nostalgic, gentle, emotional.

Style:
Premium holiday card photography, soft cinematic lighting,
realistic textures, shallow depth of field,
tasteful bokeh lights, high print-quality composition.

Constraints:
- Original artwork only
- No trademarks
- No watermarks
- No logos

Include ONLY this card text (verbatim):
"Merry Christmas — some memories never fade."
```

**Parameters**: `size=1024x1536`, `quality=medium` (use `high` if text matters)

---

## Prompt example 2: collectible toy packaging shot (Cookbook 6.3)

As a Python f-string template:

```python
prompt = f"""
Create a collectible action figure of {character_description}, in blister packaging.

Concept:
A nostalgic holiday collectible inspired by the simple toy airplanes
children used to play with during winter holidays.
Evokes warmth, imagination, and childhood wonder.

Style:
Premium toy photography, realistic plastic and painted metal textures,
studio lighting, shallow depth of field,
sharp label printing, high-end retail presentation.

Constraints:
- Original design only
- No trademarks
- No watermarks
- No logos

Include ONLY this packaging text (verbatim):
"{short_copy}"
"""
```

**Parameters**: `size=1024x1536`, `quality=medium`

**CLI example** (with variables substituted):
```bash
ccskill-gptimage generate \
  "Create a collectible action figure of a retro Japanese shiba inu mascot with a red scarf, in blister packaging. Concept: ..." \
  --size 1024x1536 --quality high \
  --output-name shiba_figure_mock
```

---

## Prompt example 3: character anchor + derived scenes (Cookbook 6.4, **two-stage workflow**)

### Part 1: anchor generation (text → image)

```
Create a children's book illustration introducing a main character.

Character:
A young, storybook-style hero inspired by a little forest outlaw,
wearing a simple green hooded tunic, soft brown boots, and a small belt pouch.
The character has a kind expression, gentle eyes, and a brave but warm demeanor.
Carries a small wooden bow used only for helping, never harming.

Theme:
The character protects and rescues small forest animals like squirrels, birds, and rabbits.

Style:
Children's book illustration, hand-painted watercolor look,
soft outlines, warm earthy colors, whimsical and friendly.
Proportions suitable for picture books (slightly oversized head, expressive face).

Constraints:
- Original character (no copyrighted characters)
- No text
- No watermarks
- Plain forest background to clearly showcase the character
```

**Parameters**: `size=1024x1536`, `quality=medium`, no input image

**CLI example**:
```bash
ccskill-gptimage generate \
  "Create a children's book illustration introducing a main character. Character: ..." \
  --size 1024x1536 --quality high \
  --output-name forest_hero_anchor
```

### Part 2: derived scene (edit path, anchor as `--reference`)

```
Continue the children's book story using the same character.

Scene:
The same young forest hero is gently helping a frightened squirrel
out of a fallen tree after a winter storm.
The character kneels beside the squirrel, offering reassurance.

Character Consistency:
- Same green hooded tunic
- Same facial features, proportions, and color palette
- Same gentle, heroic personality

Style:
Children's book watercolor illustration,
soft lighting, snowy forest environment,
warm and comforting mood.

Constraints:
- Do not redesign the character
- No text
- No watermarks
```

**Parameters**: `size=1024x1536`, `quality=medium`, one input image (the Part 1 output)

**CLI example**:
```bash
ccskill-gptimage generate \
  "Continue the children's book story using the same character. Scene: ..." \
  --reference ./generated_images/forest_hero_anchor.png \
  --size 1024x1536 --quality high \
  --output-name forest_hero_scene01
```

---

## gpt-image-2-specific notes

- **The edit path always re-renders the full canvas**, but because gpt-image-2 uses auto max fidelity, the character's appearance is strongly preserved.
- Writing `Do not redesign the character` **in every turn** is the cardinal rule for preventing drift.
- **Repeatedly verbalize** the character's appearance traits (clothing color, hairstyle, facial features) (e.g. `Same green hooded tunic`).
- The 6.4 workflow will become even more stable once the Responses API (`previous_response_id`) migration planned for Phase 0.5 lands — for now, substitute edit + `--reference`.

## Source

- Cookbook 6.2 3D pop-up holiday card / 6.3 Collectible Action Figure / 6.4 Children's Book Art with Character Consistency
- URL: https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide
- Retrieved: 2026-04-23
