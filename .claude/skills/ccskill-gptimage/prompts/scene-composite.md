# Scene Composite — Person into a new scene / multi-image compositing

Combines Cookbook 5.8 (Insert the Person Into a Scene) and 5.9 (Multi-Image Referencing and Compositing). For **extracting elements from input images and compositing them into a new scene**.

## When to use

- Campaign shoots (composite a model photo with a background photo)
- Storyboard production (place a person in various locations)
- Compositing products with lifestyle photos
- Compositing photos of a pet with the user
- Reconstructing group photos

## Cookbook quote

### 5.8 Insert Person Into Scene

> A workflow for compositing a person into a new scene. Well suited to storyboards and campaign production, where you change the background or situation while preserving the person's face and identity.

### 5.9 Multi-Image Compositing

> "Combines elements from multiple input images into a single believable composite—ideal for 'insert object/person into scene' workflows. Key is specifying what to transplant, where it goes, and what must remain unchanged while matching lighting, perspective, scale, and shadows."
> — [Cookbook 5.8 / 5.9](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide)

**Core principles**:
- State explicitly **what to transplant, where to place it, and what to preserve**
- Demand matching of light, perspective, scale, and shadows (`match lighting, perspective, scale, shadows`)
- Eliminate the "pasted-on look": `avoid pasted-on appearance`
- Explicitly preserve the background and framing

## How to write Multi-Image Inputs (Cookbook Section 2)

> "Reference each input by **index and description** ('Image 1: product photo… Image 2: style reference…') and describe how they interact ('apply Image 2's style to Image 1'). When compositing, be explicit about which elements move where."

**Required pattern**:
- **Define each input image with an index** as `Image N: description`
- **Point out in the text** which element comes from which image
- Be concrete about the target placement (`right next to the woman`, `in the background behind the table`)

---

## Prompt example 1: Insert a person into a new scene (Cookbook 5.8)

```
Generate a highly realistic action scene where this person is running away from a large, realistic brown bear attacking a campsite. The image should look like a real photograph someone could have taken, not an overly enhanced or cinematic movie-poster image.
She is centered in the image but looking away from the camera, wearing outdoorsy camping attire, with dirt on her face and tears in her clothing. She is clearly afraid but focused on escaping, running away from the bear as it destroys the campsite behind her.
The campsite is in Yosemite National Park, with believable natural details. The time of day is dusk, with natural lighting and realistic colors. Everything should feel grounded, authentic, and unstyled, as if captured in a real moment. Avoid cinematic lighting, dramatic color grading, or stylized composition.
```

**Parameters**: `size=1024x1536`, `quality=medium`, 1 input image (person source)

> **Note**: The Cookbook original spells out `input_fidelity="high"`, but with gpt-image-2 it **cannot be specified** (automatic maximum fidelity; this skill's main strips it automatically).

**CLI example**:
```bash
$CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py \
  "Generate a highly realistic action scene where this person is ..." \
  --reference ./person_source.jpg --quality high
```

---

## Prompt example 2: Two-image composite (Cookbook 5.9)

```
Place the dog from the second image into the setting of image 1, right next to the woman, use the same style of lighting, composition and background. Do not change anything else.
```

**Parameters**: `size=1024x1536`, `quality=medium`, 2 input images

**CLI example**:
```bash
$CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py \
  "Place the dog from the second image into the setting of image 1, right next to the woman, use the same style of lighting, composition and background. Do not change anything else." \
  --reference ./scene_with_woman.jpg \
  --reference ./dog.jpg \
  --quality high
```

---

## Advanced: Three or more images with explicit indices

The recommended pattern from Cookbook Section 2 (index + description).

```
Image 1: a dining room with a wooden table and warm evening lighting.
Image 2: a ceramic coffee mug with a logo.
Image 3: a plated croissant on a white plate.
Generate a photorealistic composite: place the coffee mug from Image 2 and the croissant from Image 3 on the table in the setting of Image 1. Match the lighting, shadow direction, and color temperature of Image 1. Preserve the mug's logo and the croissant's shape exactly.
Do not change the dining room, the table, the window, or other existing objects. No watermarks.
```

---

## Advanced: Place a person at a different event

Place the same model in multiple locations for campaign production.

```
Image 1: the model's reference portrait (studio shot).
Generate a highly realistic photograph of this same person standing on a coastal cliff at sunset, wearing a cream linen shirt and khaki trousers, looking out at the sea. Shot at a low angle with a 35mm lens, warm golden hour light, natural skin texture, no heavy retouching.
Preserve her exact facial identity, hair, and proportions from Image 1. Replace only her outfit (to the described attire) and place her in the new setting with matching lighting.
No watermarks, no text.
```

---

## gpt-image-2-specific notes

- **Up to 5 reference images** is the practical upper limit. More than that scatters the context
- The `input_fidelity="high"` the Cookbook frequently uses is **already in effect automatically** with gpt-image-2, so it need not be specified
- **Elements that tend to drift** during compositing: facial expression, fine details of small props, background depth
- To avoid the "pasted-on look," explicitly instruct **matching of shadow, light, and color temperature**
- Complex composites (3+ images + repositioning of many elements) require `quality=high`. At `medium` they tend to break down

## Source

- Cookbook 5.8 Insert the Person Into a Scene / 5.9 Multi-Image Referencing and Compositing
- URL: https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide
- Retrieved: 2026-04-23
