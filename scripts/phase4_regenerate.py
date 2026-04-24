#!/usr/bin/env python3
"""Phase 4: SKILL v2 effect verification — regenerate 35 capability-survey images.

Each entry has an original (v1) intent, plus a v2 prompt rewritten applying
the new SKILL principles (Cookbook Section 2 - 10 principles + use-case patterns).

Differences from v1:
- 4-part labeled structure (scene/subject/key details/constraints)
- Typography details fully specified for any text-in-image
- Explicit `Constraints:` line with no watermark / no extra text / no logos
- "photorealistic" used explicitly for photoreal targets
- Intended use labeled at the top (editorial / UI / infographic / etc.)
"""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
PY = ROOT / "venv" / "bin" / "python"
GEN = ROOT / "generate_image.py"
OUT_CAT = ROOT / "assets" / "capability-survey" / "categories" / "v2"
OUT_GRID = ROOT / "assets" / "capability-survey" / "grid" / "v2"

OUT_CAT.mkdir(parents=True, exist_ok=True)
OUT_GRID.mkdir(parents=True, exist_ok=True)

# (name, size, quality, prompt)
CATEGORIES: list[tuple[str, str, str, str]] = [
    ("01_photorealistic_portrait_woman", "1024x1024", "high",
     "Editorial fashion magazine portrait (intended use).\n"
     "Scene: a warm beige room with a large window on the right, soft natural side light, creamy background bokeh.\n"
     "Subject: photorealistic Japanese woman in her late twenties, head-and-shoulders crop, looking slightly off-camera with a gentle relaxed expression.\n"
     "Key details: cream knit sweater, fine realistic skin texture with subtle pores, natural minimal makeup, shallow depth of field, 50mm lens look, natural color grading.\n"
     "Constraints: no watermark, no extra text, no logos, no heavy retouching."),

    ("02_anime_warrior_character", "1024x1024", "high",
     "Anime character illustration (intended use).\n"
     "Scene: a misty mountain backdrop, soft falling cherry-blossom petals in foreground, plain atmospheric background.\n"
     "Subject: a young female warrior standing three-quarter view, looking forward with a calm confident expression, holding a sheathed katana at her side.\n"
     "Key details: long silver hair in a high ponytail, dark navy traditional Japanese armor with subtle gold trim, cel-shaded with clean ink linework, flat color shading with limited gradients, soft pink petals drifting across the frame.\n"
     "Constraints: no watermark, no extra text, no logos."),

    ("03_watercolor_mountain_landscape", "1536x1024", "high",
     "Traditional East-Asian watercolor landscape (intended use).\n"
     "Scene: multiple receding mountain silhouettes at dawn, a small calm reflective lake in the foreground.\n"
     "Subject: the layered mountains themselves, with gradations in blue-gray value from deep close to pale far.\n"
     "Key details: soft pink-orange sky, visible paper grain texture, generous wet-on-wet bleeding, loose confident brush strokes, classical East Asian composition balance.\n"
     "Constraints: no figures, no text, no watermark, no seal."),

    ("04_isometric_3d_reading_room", "1024x1024", "high",
     "Warm product-style isometric 3D illustration (intended use).\n"
     "Scene: a cozy reading nook viewed from above-front isometric angle, floating on a white background with centered composition.\n"
     "Subject: a wooden chair with a cream cushion, a small side table with a cup of coffee and an open book, a tall arched window with soft light.\n"
     "Key details: potted fiddle-leaf fig plant on the left, a circular wool rug under the chair, warm muted palette (cream, sage green, soft terracotta), flat shading with gentle ambient occlusion.\n"
     "Constraints: no text, no watermark, no logos, no shadows beyond soft AO."),

    ("05_ui_mockup_login_english", "1024x1536", "high",
     "Realistic SaaS login UI mockup (intended use, as if shipped).\n"
     "Scene: a clean off-white background with a very subtle top-to-bottom gradient.\n"
     "Subject: a centered rounded card (24px corner radius) containing the login form.\n"
     "Key details: exact headline \"Welcome back\" in 32pt bold sans-serif dark charcoal centered at the top of the card; subtitle \"Sign in to your workspace\" in 14pt medium gray; below, an \"Email\" input field and a \"Password\" input field with an eye icon; a small \"Forgot password?\" link in soft blue; a full-width primary \"Sign in\" button in deep navy with white 16pt bold sans-serif text; below the card a subtle \"Don't have an account? Sign up\" helper link. 8px input corner radius, pixel-perfect rendering, system sans-serif like Inter.\n"
     "Constraints: no watermark, no extra UI elements, no icons on the sides, no logos."),

    ("06_ui_mockup_settings_japanese", "1024x1536", "high",
     "Realistic iOS 18 Japanese settings screen mockup (intended use, as if shipped).\n"
     "Scene: an iPhone-shaped frameless screen on soft light-gray background.\n"
     "Subject: the settings list view with grouped rows.\n"
     "Key details: top status bar shows exact \"9:41\" time in system font on the left, signal/wifi/battery icons on the right; large navigation title \"設定\" in bold Japanese system font below the status bar; first grouped section rows — \"機内モード\" with right-side toggle OFF, \"Wi-Fi\" with right-aligned text \"FEEDTAILOR-5G\" and chevron, \"Bluetooth\" with right-aligned text \"オン\" and chevron, \"モバイル通信\" with chevron; second grouped section rows — \"通知\" (orange bell icon), \"サウンドと触覚\" (pink speaker icon), \"おやすみモード\" (purple moon icon), \"スクリーンタイム\" (indigo hourglass icon), each icon in a small rounded-square colored tile; subtle 1px separators between rows; sharp pixel-perfect rendering.\n"
     "Constraints: all Japanese labels rendered verbatim in quotes above; no watermark, no extra text outside the specified labels, no logos."),

    ("07_infographic_quarterly_revenue", "1024x1536", "high",
     "One pitch-deck-style infographic slide (intended use, board deck quality).\n"
     "Scene: very light gray background with generous padding, single-slide layout.\n"
     "Subject: a vertical bar chart comparing 4 quarters of revenue.\n"
     "Key details: headline exactly \"FY2026 Quarterly Revenue\" in bold 40pt sans-serif (Inter-like), dark navy, centered at the top; subtitle exactly \"Unit: million yen\" in 14pt medium gray below; a vertical bar chart with 4 bars labeled \"Q1\", \"Q2\", \"Q3\", \"Q4\" along the x-axis, values \"12\", \"18\", \"27\", \"35\" rendered above each bar in 18pt bold; bars in graduated teal-to-deep-blue with subtle drop shadow; y-axis with gridlines at 0, 10, 20, 30, 40; right side: a small coral annotation arrow with exact text \"+192% YoY\" in 16pt bold coral; clean data hierarchy, polished spacing.\n"
     "Constraints: render every text string above verbatim, no extra characters; no clip art, no stock photography, no gradients beyond the bar color ramp, no decorative elements, no watermark, no logos."),

    ("08_flowchart_microservices_architecture", "1024x1024", "high",
     "Tech architecture documentation diagram (intended use).\n"
     "Scene: a clean light-gray background with generous spacing.\n"
     "Subject: a microservices architecture flowchart.\n"
     "Key details: centered top rounded-rectangle labeled exactly \"API Gateway\" in deep blue; three downward arrows fan out to three rounded-rectangles labeled exactly \"Auth Service\", \"Order Service\", \"Payment Service\" in teal; each service connects downward to a database cylinder labeled exactly \"auth_db\", \"orders_db\", \"payments_db\"; on the right, a separate rounded-rectangle labeled exactly \"Message Queue (Kafka)\" connected from each service by dotted arrows; SVG-style flat shapes, sharp sans-serif typography, no shadows.\n"
     "Constraints: render labels verbatim, no other text, no watermark, no logos."),

    ("09_food_photo_tonkotsu_ramen", "1024x1024", "high",
     "Photorealistic food photography (intended use, editorial food magazine).\n"
     "Scene: a dark wooden table with subtle wood grain, soft warm natural light from upper-left, gentle steam rising.\n"
     "Subject: overhead shot of a bowl of tonkotsu ramen.\n"
     "Key details: rich creamy white broth, curly noodles, two slices of chashu pork, a soft-boiled egg cut in half showing orange yolk, green scallions, half a nori sheet, sprinkle of black sesame, a small mound of finely chopped white onion; chopsticks resting on a ceramic chopstick rest beside the bowl; a small dish of red pickled ginger; photorealistic, shallow depth of field softening the bowl edges.\n"
     "Constraints: no watermark, no extra text, no logos, no cutlery other than the described chopsticks."),

    ("10_architectural_render_modern_house", "1536x1024", "high",
     "Architectural visualization exterior render (intended use).\n"
     "Scene: golden-hour outdoor setting, sky in peach-to-pale-blue gradient, warm low sun raking from the right casting long soft shadows.\n"
     "Subject: a modern minimalist two-story house, photorealistic architectural render.\n"
     "Key details: clean exposed concrete and warm wood facade, floor-to-ceiling glazing revealing softly lit interior, flat roof with subtle overhang, integrated garage on the left, a thin reflection pool along the front, low manicured grass, a single mature olive tree, smooth concrete path in the foreground, sharp material rendering.\n"
     "Constraints: no people, no cars, no watermark, no extra text, no logos."),

    ("11_hand_drawn_pen_sketch_tokyo_alley", "1024x1024", "high",
     "Urban-sketcher travel-journal illustration (intended use).\n"
     "Scene: a narrow Tokyo back alley at dusk, deliberate watercolor bleed at the edges, visible paper grain.\n"
     "Subject: the alley view with a small izakaya on the right.\n"
     "Key details: confident black ink pen lines with pressure variation, light watercolor wash in warm sepia and muted teal accents, red lanterns above the izakaya, a bicycle leaning against a wall, overhead tangled power lines, a softly glowing vending machine on the left, loose cross-hatching for shadows.\n"
     "Constraints: no caption text, no watermark, no signature, no logos."),

    ("12_comic_4koma_japanese_programmer", "1024x1536", "high",
     "Traditional Japanese 4-koma manga strip (intended use).\n"
     "Scene: vertical layout with 4 equal-size panels stacked top-to-bottom, clean black ink linework on white, each panel bordered with a solid black rectangle.\n"
     "Subject: a young female programmer character, consistent across all 4 panels (same short bob hair, same round glasses, same gray hoodie).\n"
     "Key details: above panel 1 a bold Japanese gothic title exactly \"プログラマあるある\"; Panel 1 — she stares at a laptop, speech bubble exactly \"なぜか動いた…!\"; Panel 2 — same character with a thoughtful hand-on-chin pose, speech bubble exactly \"なぜ動くんだろう?\"; Panel 3 — she types on the laptop, speech bubble exactly \"ちょっと整理しよう\"; Panel 4 — she stares at the broken laptop with a deadpan face, speech bubble exactly \"なぜ動かない…!?\"; soft screentone on backgrounds; tiny attribution bottom-right exactly \"ccskill gptimage\".\n"
     "Constraints: render every Japanese string verbatim, no extra characters; no watermark outside the attribution; same character appearance in every panel."),

    ("13_logo_abstract_mark_vectra", "1024x1024", "high",
     "Original non-infringing brand logo for a fictional AI infrastructure startup (intended use).\n"
     "Scene: plain white background, centered composition, generous padding.\n"
     "Subject: a geometric logo mark plus wordmark for a company called VECTRA.\n"
     "Key details: mark is a single continuous clean line forming a stylized upward arrow that loops elegantly into a circle at its base, suggesting iteration and ascent; primary color deep indigo #2a2d6e; a single warm amber #f4a020 accent dot at the tip of the arrow; to the right of the mark, the wordmark exactly \"VECTRA\" in a clean modern geometric sans-serif (Inter-like), slight letter-spacing, deep indigo; flat vector style, sharp clean edges, no gradients.\n"
     "Constraints: original design, no trademarks, no watermark, no extra text beyond the wordmark, no taglines."),

    ("14_japanese_poster_vertical_tategaki", "1024x1536", "high",
     "Editorial magazine Japanese tategaki poster (intended use).\n"
     "Scene: vertical canvas with deep indigo #0e1a3a background and very subtle paper-grain texture, generous negative space.\n"
     "Subject: a single tategaki (vertical) Japanese title column set from top-right to bottom.\n"
     "Key details: main title exactly \"未来は描かれるものではない、計画されるものだ。\" rendered as a single vertical right-to-left column in elegant Japanese serif (Mincho-like), warm ivory white, 60-72pt; punctuation (、 。) rotated appropriately for vertical reading; to the left of the title, a smaller horizontal English subtitle exactly \"The future is not drawn, it is planned.\" in thin sans-serif, 14pt, ivory; a thin gold horizontal rule above and below the English subtitle; bottom-right tiny attribution exactly \"ccskill-gptimage / 2026\" in 10pt soft gold sans-serif.\n"
     "Constraints: every text string rendered verbatim with every character and punctuation mark preserved; no watermark; no other text anywhere."),

    ("15_abstract_generative_ribbons", "1024x1024", "high",
     "Gallery-quality generative abstract artwork (intended use).\n"
     "Scene: a deep midnight indigo void space with subtle volumetric atmosphere.\n"
     "Subject: flowing organic ribbons of color suspended mid-motion, suggesting liquid mercury caught in time.\n"
     "Key details: ribbons in graduated coral, soft peach, lavender, with a single thread of warm gold; smooth volumetric lighting, specular highlights catching on ribbon surfaces, extremely high-detail surface micro-texture, dreamlike quality, subtle depth of field, balanced weight, centered composition.\n"
     "Constraints: no text, no figures, no recognizable objects, no watermark, no logos."),

    ("16_daily_morning_kitchen", "1024x1024", "high",
     "Lifestyle photography editorial snapshot (intended use).\n"
     "Scene: a Japanese home kitchen in the morning, soft morning side-light from a window with sheer linen curtain.\n"
     "Subject: photorealistic hands of a woman pouring drip coffee into a glass carafe, shot from a top-down 45-degree angle.\n"
     "Key details: on the counter — a small wooden cutting board with a half-cut peach, an open notebook with a pen, a ceramic mug, a sprig of basil; background slightly out of focus showing wooden cabinets and a hanging copper pot; warm earthy color grade, fine film grain, 35mm film aesthetic, close composition.\n"
     "Constraints: no watermark, no extra text, no logos."),

    ("17_nature_misty_cedar_forest", "1536x1024", "high",
     "Cinematic landscape photography (intended use, National Geographic caliber).\n"
     "Scene: a primeval forest interior at dawn with drifting fog.\n"
     "Subject: tall ancient cedar trunks rising into mist.\n"
     "Key details: photorealistic rendering, beams of soft golden god-rays piercing through the canopy, lush ferns and moss-covered stones beside a tiny stream in the foreground, cool blue-green palette with warm light shafts, hyper-detailed bark texture, sharp focus throughout.\n"
     "Constraints: no figures, no trails, no structures, no text, no watermark."),

    ("18_nature_volcanic_coast_dawn", "1536x1024", "high",
     "ND-filter long-exposure seascape photography (intended use).\n"
     "Scene: a volcanic black-rock coastline at dawn, distant sea stacks fading into mist.\n"
     "Subject: the jagged rocks and silk-smooth motion-blurred waves, with a single weathered cypress tree silhouetted on a cliff edge on the right.\n"
     "Key details: photorealistic rendering, crashing turquoise waves frozen in silk-smooth long-exposure motion, soft pastel sunrise sky in pink-orange-violet gradient, hyper-real rock texture, fine water spray detail, professional landscape composition.\n"
     "Constraints: no figures, no boats, no text, no watermark."),

    ("19_urban_tokyo_rainy_night", "1536x1024", "high",
     "Cinematic street photography (intended use).\n"
     "Scene: a Tokyo Shibuya-style scramble crossing right after rain at night, wet asphalt mirroring neon signs.\n"
     "Subject: the crossing in a medium-wide shot from a slight elevation, crowds with umbrellas in slight motion blur, taxis with glowing red brake lights.\n"
     "Key details: photorealistic, Japanese kanji storefront neons in deep red, electric blue, warm yellow reflecting on the wet pavement; cinematic teal-orange color grade; atmospheric depth with soft rain haze in the background; authentic Tokyo nighttime mood.\n"
     "Constraints: no recognizable brand names or logos, no readable specific text on signs (kanji shapes only), no watermark."),

    ("20_vehicle_cafe_racer_motorcycle", "1536x1024", "high",
     "High-end automotive photography (intended use).\n"
     "Scene: a cobblestone alleyway at golden hour, worn brick walls on both sides, soft warm sun raking from the left casting long shadows.\n"
     "Subject: a vintage cafe-racer motorcycle parked in the center, photorealistic.\n"
     "Key details: matte deep British-Racing-Green paint, brown leather seat, polished chrome exhaust, spoke wheels; a small wooden crate beside the bike with an old leather helmet on top; shallow depth of field with background bokeh; cinematic composition.\n"
     "Constraints: no people, no text, no brand logos on the bike, no watermark."),

    ("21_sports_rock_climbing_action", "1024x1536", "high",
     "Sports action photography (intended use).\n"
     "Scene: a steep overhanging granite wall at sunset, sunset golden-orange light raking across the textured rock, valley below in soft bokeh.\n"
     "Subject: a male rock climber caught mid-move reaching for the next hold, full body visible in powerful dynamic stance, sharp focus on the climber.\n"
     "Key details: photorealistic; chalk-dusted hands, red climbing shoes, a green tank top; body muscles engaged; light catching the chalk cloud; shallow depth of field blurring the distant landscape; peak-action moment captured.\n"
     "Constraints: no other climbers, no text, no watermark, no logos."),

    ("22_pet_shiba_inu_autumn", "1024x1024", "high",
     "Pet portrait photography (intended use).\n"
     "Scene: a Japanese autumn park with soft warm afternoon light, fallen red maple leaves on the ground, golden trees in blurred bokeh background.\n"
     "Subject: a Shiba Inu dog sitting, looking slightly off-camera with a gentle relaxed expression.\n"
     "Key details: photorealistic; fine fur detail in honey-tan and white, alert triangular ears, warm brown eyes, mouth slightly open in a relaxed smile; shallow depth of field; eye-level composition; catch-light in the eyes.\n"
     "Constraints: no other animals, no humans, no text, no watermark, no collar tags with writing."),

    ("23_wildlife_red_fox_snow", "1024x1024", "high",
     "National Geographic-style wildlife photography (intended use).\n"
     "Scene: a snowy boreal forest at dawn, dark spruce trees in soft bokeh, low golden light catching ice crystals in the foreground.\n"
     "Subject: a wild red fox standing alert mid-step, looking off-camera to the left, with visible white breath in the cold air.\n"
     "Key details: photorealistic; vivid orange coat contrasting with white snow, fine fur texture, snow on the fox's shoulders, ultra-sharp focus on the eyes, subtle motion feel.\n"
     "Constraints: no other animals, no humans, no text, no watermark."),

    ("24_line_drawing_fashion_sketch", "1024x1024", "high",
     "Fashion technical line illustration (intended use).\n"
     "Scene: pure white background, plenty of negative space, centered composition.\n"
     "Subject: a young woman in a flowing dress mid-step, three-quarter angle.\n"
     "Key details: single-weight clean confident black ink lines, no shading, no fill, continuous-line feel; hair flowing, dress hem catching air, relaxed hands; elegant outlines only.\n"
     "Constraints: no color, no shading, no signature, no text, no watermark."),

    ("25_sumi_e_heron_ink_wash", "1536x1024", "high",
     "Traditional Japanese sumi-e ink wash painting (intended use).\n"
     "Scene: aged rice paper surface with visible texture and subtle ink bleed, abundant negative space.\n"
     "Subject: a solitary heron standing in shallow water amid a few delicate reeds, looking down.\n"
     "Key details: bold confident brush strokes for the heron's body in deep black ink, soft gray washes for water reflection and distant mist, ink gradation from rich dark to pale wash; a single small red hanko seal in the lower-right corner; minimalist classical East Asian composition.\n"
     "Constraints: no modern elements, no English text, no watermark, only the one hanko seal."),

    ("26_kids_crayon_doodle_family", "1024x1024", "high",
     "A genuine children's crayon-and-marker doodle photographed from above (intended use, keepsake photo).\n"
     "Scene: a sheet of slightly crumpled white paper with subtle wrinkles and faint pencil shadow marks, photographed top-down.\n"
     "Subject: the child's drawing occupying most of the paper.\n"
     "Key details: a cheerful family of three holding hands in front of a triangular-roof house — mom in pink dress, dad in blue, child in red; a bright yellow sun with rays in the upper-left corner; two fluffy white clouds; two simple flowers with round centers; a smiling cat on the right; wobbly imperfect child-like lines, vibrant uneven crayon textures, mixed crayon and felt-tip marker strokes.\n"
     "Constraints: no text on the drawing, no adult-style lettering, no signature, no watermark."),
]

# Grid: same intent across 9 cells (3 sizes × 3 qualities) but with v2 prompt rewrite.
GRID_PROMPT_V2 = (
    "Editorial portrait poster for a lifestyle magazine (intended use).\n"
    "Scene: a sunlit cafe interior with a large window on the right, soft warm afternoon light, creamy bokeh of the cafe beyond.\n"
    "Subject: a Japanese woman in her twenties reading a book, three-quarter view, partially lit by the window, gentle contemplative expression.\n"
    "Key details: shallow depth of field; top of the poster shows exact headline \"本と珈琲\" in large serif Japanese font (Mincho-like), dark charcoal, 56pt, centered; below the headline a small subtitle exactly \"Tokyo, Spring 2026\" in thin English sans-serif, 14pt, medium gray; generous negative space; magazine-quality composition.\n"
    "Constraints: render text strings verbatim; no watermark, no logos, no extra text beyond the two specified strings."
)

GRID_CELLS: list[tuple[str, str, str]] = [
    ("grid_book_coffee_1024x1024_low",    "1024x1024", "low"),
    ("grid_book_coffee_1024x1024_medium", "1024x1024", "medium"),
    ("grid_book_coffee_1024x1024_high",   "1024x1024", "high"),
    ("grid_book_coffee_1024x1536_low",    "1024x1536", "low"),
    ("grid_book_coffee_1024x1536_medium", "1024x1536", "medium"),
    ("grid_book_coffee_1024x1536_high",   "1024x1536", "high"),
    ("grid_book_coffee_1536x1024_low",    "1536x1024", "low"),
    ("grid_book_coffee_1536x1024_medium", "1536x1024", "medium"),
    ("grid_book_coffee_1536x1024_high",   "1536x1024", "high"),
]


def run_one(prompt: str, size: str, quality: str, output_dir: Path, output_name: str) -> int:
    existing = output_dir / f"{output_name}.png"
    if existing.exists() and existing.stat().st_size > 0:
        print(f"\n[{output_name}] skip (already exists)")
        return 0
    cmd = [
        str(PY), str(GEN), prompt,
        "--size", size,
        "--quality", quality,
        "--output", str(output_dir),
        "--output-name", output_name,
    ]
    print(f"\n[{output_name}] size={size} quality={quality}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[Error] {output_name}: {res.stderr.strip() or res.stdout.strip()}")
        return 1
    # print the [Success]/[Revised] lines from stdout
    for line in res.stdout.splitlines():
        if line.startswith("[Success]") or line.startswith("[Revised]") or line.startswith("[Warning]"):
            print(f"  {line}")
    return 0


def main(argv: list[str]) -> int:
    failures = 0
    total = len(CATEGORIES) + len(GRID_CELLS)
    done = 0
    start = time.time()

    # Filter if a prefix is provided, e.g. `phase4_regenerate.py 07` runs only matching ones.
    prefix = argv[1] if len(argv) > 1 else None

    for name, size, quality, prompt in CATEGORIES:
        if prefix and not name.startswith(prefix):
            done += 1
            continue
        failures += run_one(prompt, size, quality, OUT_CAT, name)
        done += 1
        elapsed = time.time() - start
        print(f"  progress: {done}/{total}  elapsed: {elapsed:.0f}s")

    for name, size, quality in GRID_CELLS:
        if prefix and not name.startswith(prefix):
            done += 1
            continue
        failures += run_one(GRID_PROMPT_V2, size, quality, OUT_GRID, name)
        done += 1
        elapsed = time.time() - start
        print(f"  progress: {done}/{total}  elapsed: {elapsed:.0f}s")

    elapsed = time.time() - start
    print(f"\n=== Phase 4 regeneration complete ===")
    print(f"  success: {total - failures}/{total}")
    print(f"  elapsed: {elapsed:.0f}s")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
