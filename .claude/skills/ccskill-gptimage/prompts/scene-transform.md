# Scene Transform — Weather / time-of-day change / object removal

Combines Cookbook 5.6 (Lighting and Weather Transformation) and 5.7 (Object Removal). The shared design is **"preserve composition, identity, and geometry; change only the environmental conditions or a specific element."**

## When to use

- Re-lighting a landmark photo to "evening," "a snowy day," or "a rainy day"
- Seasonal variants of an ad visual (spring/summer/autumn/winter)
- Erasing an unwanted subject (passersby, power lines, clutter, unneeded objects)
- Cleaning up a product photo (remove extraneous items on the table)

## Cookbook quote

### 5.6 Lighting / Weather Transformation

> "Re-stage photos for different moods, seasons, or times of day while preserving scene composition, identity, geometry, camera angle, and object placement."

### 5.7 Object Removal

> "Object removal is the edit use case for deleting specific elements from a scene while completely preserving everything else (person identity, lighting, background)."
> — [Cookbook 5.6 / 5.7](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide)

**Core principles**:
- Write **both what to change and what to preserve** (the "Constraints" principle in Cookbook Section 2)
- 5.6 **changes only environmental conditions**: light direction, shadows, atmosphere, precipitation, wet ground
- 5.7 **changes only the removal target**: `Do not change anything else`

---

## Prompt example 1: Weather / time-of-day change (Cookbook 5.6)

```
Make it look like a winter evening with snowfall.
```

**Parameters**: `size=1024x1536`, `quality=medium`, 1 input image

**CLI example**:
```bash
$CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py \
  "Make it look like a winter evening with snowfall." \
  --reference ./sunset_scene.jpg --quality high
```

> **Note**: The Cookbook original spells out `input_fidelity="high"`, but with gpt-image-2 it **cannot be specified** (automatic maximum fidelity; this skill's main strips it automatically).

### A more specific pattern

```
Transform this scene to a snowy winter evening at dusk:
- Time of day: shortly after sunset, cool blue hour
- Weather: gentle snowfall, snow accumulating on flat surfaces
- Lighting: cool ambient light with warm interior windows
- Atmosphere: slight haze, soft bokeh from streetlamps
Preserve: camera angle, composition, subject positions, buildings and landmarks, people's identities and clothing silhouettes.
Do not add or remove any elements. No watermarks.
```

---

## Prompt example 2: Object removal (Cookbook 5.7)

```
Remove the flower from man's hand. Do not change anything else.
```

**Parameters**: `size=1024x1536`, `quality=medium`, 1 input image

**CLI example**:
```bash
$CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py \
  "Remove the flower from man's hand. Do not change anything else." \
  --reference ./man_with_flower.jpg --quality high
```

### A stronger "preserve" instruction

```
Remove the cardboard box on the left side of the kitchen counter. Fill the area naturally with the same counter material (white marble) that is visible elsewhere in the scene. Do not change any other object, person, lighting, shadow, or background element. Preserve the exact camera angle, framing, and all labels/texts on visible products and appliances.
```

---

## Advanced: Erase the crowd from a busy landmark

```
Remove all the tourists from the scene while keeping the landmark, architecture, foreground, sky, and lighting exactly as is. Fill the cleared ground naturally with the same pavement/floor material visible nearby. Do not change time of day, weather, or camera angle. No watermarks.
```

---

## Advanced: Big changes like spring→autumn, day→night

```
Change this scene from summer daytime to autumn early evening (golden hour).
- Foliage: transform the green trees to warm autumn colors (red, orange, yellow)
- Light: warm golden hour light from low sun on the right
- Ground: add a few scattered fallen leaves on the path
Preserve: camera angle, composition, all buildings, all people's positions and clothing silhouettes, road layout.
No watermarks.
```

---

## gpt-image-2-specific notes

- Thanks to **automatic maximum fidelity**, people, buildings, and signage text are strongly preserved
- However, the edit path is a **full-canvas redraw**. There is no pixel-perfect match of fine detail
- In weather changes, **shadow direction changes** — the model auto-adjusts physically consistent shadows
- In object removal, **background fill is the Cookbook's forte**. It fills in well even with complex backgrounds
- Issuing multiple changes at once (weather + add person + removal) lowers accuracy. **One change per pass** is the official recommendation (Section 2 "Iterate Instead of Overloading")

## Source

- Cookbook 5.6 Lighting and Weather Transformation / 5.7 Object Removal
- URL: https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide
- Retrieved: 2026-04-23
