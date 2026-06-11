# Photorealism / Scenes with Historical Context

Combines Cookbook 4.3 and 4.4. The shared challenges are **"natural, like a real photograph"** and **"reproducing the context of an era and place."**

## When to use

- Portrait / candid photography / people shots for ads (avoiding a studio look)
- Scenes set against a specific era or historical event (leveraging the model's world knowledge)
- Documentary-style visuals (journalism, documentary)

## Core principles (Cookbook quotes)

> "To get believable photorealism, prompt the model as if a real photo is being captured in the moment. Use photography language (lens, lighting, framing) and explicitly ask for real texture (pores, wrinkles, fabric wear, imperfections). Avoid words that imply studio polish or staging. When detail matters, set quality='high'."
> — [Cookbook 4.3](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide)

**Tips**:
- **Put `photorealistic` explicitly in the prompt** (officially recommended by the Cookbook; it strongly invokes photorealistic mode)
- Use photography terms: focal length (`50mm lens`), framing (`medium close-up at eye level`), film grain (`subtle film grain`), depth of field (`shallow depth of field`)
- Be specific about texture: `pores, wrinkles, fabric wear, imperfections`
- Phrases to avoid a studio look: `No glamorization, no heavy retouching. honest and unposed.`

---

## Prompt example 1: A candid portrait (Cookbook 4.3)

```
Create a photorealistic candid photograph of an elderly sailor standing on a small fishing boat.
He has weathered skin with visible wrinkles, pores, and sun texture, and a few faded traditional sailor tattoos on his arms.
He is calmly adjusting a net while his dog sits nearby on the deck. Shot like a 35mm film photograph, medium close-up at eye level, using a 50mm lens.
Soft coastal daylight, shallow depth of field, subtle film grain, natural color balance.
The image should feel honest and unposed, with real skin texture, worn materials, and everyday detail. No glamorization, no heavy retouching.
```

**Parameters**: `size=1024x1536`, `quality=medium` — for close-up portraits where facial detail is the priority, raise to `high`

**CLI example**:
```bash
ccskill-gptimage generate \
  "Create a photorealistic candid photograph of an elderly sailor ..." \
  --size 1024x1536 --quality high
```

---

## Prompt example 2: Leveraging historical context (Cookbook 4.4)

With the model's world knowledge, it infers a culturally accurate scene from the date and place even without explicitly saying "Woodstock."

```
Create a realistic outdoor crowd scene in Bethel, New York on August 16, 1969.
Photorealistic, period-accurate clothing, staging, and environment.
```

**Parameters**: `size=1024x1536`, `quality=medium`

**Variation** (Japanese context): the model's world knowledge works for Japanese cultural events too.

```
Create a photorealistic wide street scene in Tokyo's Shibuya on the night of 1999-12-31.
Period-accurate signage, fashion, and crowd atmosphere. No modern smartphones.
```

---

## Design pattern (reflecting the people/pose principles of Cookbook Section 2)

Cookbook Section 2 "People, Pose, and Action" original text:

> "For people in scenes, describe scale, body framing, gaze, and object interactions. Examples: 'full body visible, feet included,' 'child-sized relative to the table,' 'looking down at the open book, not at the camera.'"

Elements to make specific:
- **Scale**: how large the subject is within the frame (e.g. `full body visible, feet included`)
- **Body framing**: the framing (e.g. `medium close-up`)
- **Gaze**: the direction of the gaze (e.g. `looking down at the open book, not at the camera`)
- **Object interactions**: what the subject is doing (e.g. `calmly adjusting a net`)

---

## Empty / null state declaration

gpt-image-2 tends to **fill in content on its own** when something is left "empty" (the model supplies "mug = a drink," "room = people"). Verified (2026-04-24 dogfooding): when asked to draw an empty Thermos mug, brown liquid appeared on its own. Adding `mug is empty, no liquid visible inside` correctly produced an empty one.

**Tip — declare a null state affirmatively, not as a negation**:

- ❌ `do not show people in the room` (negations work weakly)
- ✅ `the room is empty, no people present, only furniture visible` (affirmatively declaring "the state of being empty")

Variations: write `empty plate`, `empty glass`, `blank canvas`, `unoccupied bench`, etc. as "this is in an empty state" rather than "what is absent." The same applies when drawing a "deserted street corner" to convey a cultural atmosphere (see [`cultural-atmosphere.md`](cultural-atmosphere.md)).

---

## gpt-image-2-specific notes

- For photorealistic close-ups of faces and skin, `quality=high` is recommended (at `medium` the skin texture can look slightly CG)
- When bringing in a reference photo, **identity is automatically preserved at maximum fidelity** (no need to specify `input_fidelity`)
- When depicting a historical scene, **pinning down the date, place, and event name is important**. If vague, the output tends to be "plausible but wrong"

## Source

- Cookbook 4.3 Photorealistic / 4.4 World knowledge
- URL: https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide
- Retrieved: 2026-04-23
