# UI Mockups

Cookbook 4.8. UI mockups for mobile/web apps. The single biggest tip is to **"describe it as a shipped product"** (avoid concept-art vocabulary).

## When to use

- Design sketches for mobile apps (with iPhone / Android frames)
- Dashboards for web services
- Screen mockups for product demos
- UI visualizations for sales materials

## Cookbook quote

> "UI mockups should be described as if you're describing an implemented product: focus on layout, hierarchy, spacing, and actual interface elements. Avoid 'concept art' or 'design sketch' language—instead, describe it as if the app already ships."
> — [Cookbook 4.8](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide)

**Tips**:
- Avoid `design sketch` / `mockup concept` → write `real, well-designed, beautiful app`
- Be specific about layout: header, list, sections, information hierarchy
- Use real UI elements (vendor list, Today's specials, location/hours) with fictional brand names
- A device-frame instruction (`Place the UI mockup in an iPhone frame.`) makes the final asset easier to use

---

## Prompt example (Cookbook 4.8)

```
Create a realistic mobile app UI mockup for a local farmers market.
Show today's market with a simple header, a short list of vendors with small photos and categories, a small "Today's specials" section, and basic information for location and hours.
Design it to be practical, and easy to use. White background, subtle natural accent colors, clear typography, and minimal decoration.
It should look like a real, well-designed, beautiful app for a small local market.
Place the UI mockup in an iPhone frame.
```

**Parameters**: `size=1024x1536` (mobile portrait), `quality=medium` (use `high` if there are many small labels)

**CLI example**:
```bash
$CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py \
  "Create a realistic mobile app UI mockup for a local farmers market. ..." \
  --size 1024x1536 --quality high \
  --output-name farmers_app_mock
```

---

## Variation: web dashboard

```
Create a realistic desktop web app dashboard UI for a DMARC monitoring SaaS called "MailGuard".
Layout: left sidebar with navigation items ("Overview", "Reports", "Domains", "Alerts", "Settings"), top bar with search and user avatar, main content area with:
- 4 small KPI cards (Pass Rate 94%, Fail 6%, Quarantine 0%, Total Messages 1.2M)
- A line chart showing pass rate trends over 30 days
- A table of recent domains with status badges
Design it like a real, well-designed, shipping product. Dark theme with teal accents, clean sans-serif typography (like Inter), ample whitespace.
No watermarks, no extra text, no stock imagery.
Render at standard desktop browser proportions.
```

**Parameters**: `size=1536x1024` (landscape PC screen), `quality=high` (essential for dashboards, which have lots of small text)

---

## Pattern that pops more with an iPhone frame

The Cookbook's original `Place the UI mockup in an iPhone frame.` works well when you want a **device mockup rather than a flat screenshot**.

```
Create a realistic product hero image showing the MailGuard mobile app UI inside an iPhone 15 Pro frame.
The phone is standing slightly tilted on a minimal desk, with soft morning light from a window.
Inside the screen: the app's main dashboard with DMARC alerts and pass-rate visualization.
Background: clean Scandinavian office, shallow depth of field, photorealistic.
```

**Parameters**: `size=1024x1536`, `quality=high`

---

## gpt-image-2-specific notes

- **`quality=high` is nearly mandatory for UI mockups.** At `medium`, small text and icons break down.
- Mobile UI is naturally portrait (`1024x1536`); web UI is naturally landscape (`1536x1024`).
- **Avoid prompts that imitate real-brand UIs** (`like Instagram`, `like Slack`, etc.) — build with your own brand.
- Write precise figures (`94%`, `1.2M`) **directly** in the prompt. Left to the model, the numbers drift.
- The Cookbook 4.8 `in an iPhone frame` instruction is powerful — it turns the result into an actual device mockup.

## Source

- Cookbook 4.8 UI Mockups
- URL: https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide
- Retrieved: 2026-04-23
