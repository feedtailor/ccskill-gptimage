# ccskill-gptimage Image Generation Skill

[日本語 README](README.ja.md)

A Claude Code image-generation skill powered by OpenAI **gpt-image-2** (ChatGPT Images 2.0). Also usable as a standalone CLI.

Sister skill: [ccskill-nanobanana](https://github.com/feedtailor/ccskill-nanobanana) (Gemini 3 Pro Image)

## Features

- **Multilingual text rendering** — Japanese (kanji/kana) + emoji posters and banners come out readable in one shot
- **Agentic reasoning** — first agentic image generation model; plans structure before drawing
- **Reference-image editing** — base new images on existing ones via `--reference`
- **Mask editing (inpainting)** — replace parts of existing images
- **Auto metadata sidecar** — prompt, `revised_prompt`, parameters saved as JSON
- **Cost-aware defaults** — built-in knowledge that portrait `high` is cheaper than square `high`

## Examples

A handful of one-shot examples, all generated at `--quality high` with **no regeneration and no human prompt-writing** (Claude composed the prompts from intent + SKILL.md). The full **35-image gallery** including a 3×3 resolution-quality cost grid is at [`docs/gallery.md`](docs/gallery.md) →

<table>
<tr>
  <td align="center" width="33%"><img src="assets/capability-survey/categories/v2/01_photorealistic_portrait_woman.png" width="260" alt="Photoreal portrait"></td>
  <td align="center" width="33%"><img src="assets/capability-survey/categories/v2/19_urban_tokyo_rainy_night_v3.png" width="260" alt="Tokyo Shibuya scramble crossing at rainy night"></td>
  <td align="center" width="33%"><a href="docs/gallery.md"><img src="assets/capability-survey/categories/v2/18_nature_volcanic_coast_dawn.png" width="260" alt="See the full gallery"></a></td>
</tr>
<tr>
  <td align="center" width="33%"><img src="assets/capability-survey/categories/v2/24_line_drawing_fashion_sketch.png" width="260" alt="Fashion line drawing"></td>
  <td align="center" width="33%"><img src="assets/capability-survey/categories/v2/14_japanese_poster_vertical_tategaki.png" width="260" alt="Vertical Japanese poster"></td>
  <td align="center" width="33%"><img src="assets/capability-survey/categories/v2/06_ui_mockup_settings_japanese.png" width="260" alt="iOS Settings UI in Japanese"></td>
</tr>
</table>

35/35 succeeded in one shot. Total cost for the entire survey: **¥910 ($6.04)**.

## Setup

### Requirements (two options)

This skill works if either backend is available:

**Option A: ChatGPT subscription + Codex CLI (recommended — no API key needed)**
- **Python 3.10+**
- **ChatGPT subscription** (Plus or higher)
- **[Codex CLI](https://github.com/openai/codex) installed and `codex login` completed**
- → No API key, no extra billing (covered by your subscription quota)

**Option B: OpenAI API key (classic)**
- **Python 3.10+**
- **OpenAI API key** + **Organization Verification completed** (otherwise 403)
- → Pay-as-you-go (a few cents to tens of cents per image)

If both are available, `--backend auto` (default) prefers Codex and falls back to API on failure.

### 1. Clone

```bash
cd /path/to/your-projects
git clone https://github.com/feedtailor/ccskill-gptimage.git
cd ccskill-gptimage
```

### 2. Set up your backend

**Option A (Codex CLI):**

```bash
# Install Codex CLI (Homebrew)
brew install codex
# Log in with your ChatGPT account
codex login
# Verify: should print OK if tokens.access_token is present
cat ~/.codex/auth.json | python -c "import sys,json;print('OK' if json.load(sys.stdin).get('tokens',{}).get('access_token') else 'NG')"
```

**Option B (API key):**

1. Issue a key at [OpenAI Platform](https://platform.openai.com/api-keys)
2. Confirm your Organization is **Verified** (Settings → General → Verifications)
3. Billing must be enabled (`gpt-image-2` has no free tier)

### 3. Configure environment (Option B only)

```bash
cp .env.example .env
```

Edit `.env`:
```
OPENAI_API_KEY=sk-...
```

### 4. Install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

### 5. Set environment variable (when used as a skill)

Add to `.bashrc` / `.zshrc`:
```bash
export CCSKILL_GPTIMAGE_DIR="/path/to/ccskill-gptimage"
```

## Usage

### Direct CLI

```bash
source venv/bin/activate
python generate_image.py "a coastal sunset"
```

### Options

| Option | Description | Default |
|---|---|---|
| `--size` | Output size (`auto`/`1024x1024`/`1024x1536`/`1536x1024`) | `1024x1024` |
| `--quality` | Quality (`auto`/`low`/`medium`/`high`) | `auto` |
| `--background` | Background (`auto`/`opaque`). `transparent` requires `--model gpt-image-1.5` | `auto` |
| `--output-format` | Output format (`png`/`jpeg`/`webp`) | `png` |
| `--output-compression` | Compression for jpeg/webp (0-100) | none |
| `--output` | Output directory | `./generated_images` |
| `--reference` | Reference image (repeatable) | none |
| `--mask` | Mask image (transparent area = editable) | none |
| `--input-fidelity` | Not needed for gpt-image-2 (always max fidelity). For `gpt-image-1.5` only | none |
| `--moderation` | Moderation (`auto`/`low`) | `auto` |
| `--backend` | Generation backend (`auto`/`codex`/`api`). `auto` prefers Codex, falls back to API on failure | `auto` |

### Examples

```bash
# Basic
python generate_image.py "A minimalist fox logo, flat vector, navy and gold"

# Japanese poster
python generate_image.py 'A minimalist editorial poster with the exact title "腹落ちDMARC" in large serif Japanese font, dark navy background' --size 1024x1536 --quality high

# Edit using a reference (background swap)
python generate_image.py "Place the same fox logo on a deep navy background with subtle gold sparkles. Preserve the fox's pose and proportions from the reference." --reference ./logo.png --quality medium

# Multi-reference composition
python generate_image.py "Photorealistic gift basket on white" --reference ./a.png --reference ./b.png --reference ./c.png

# Mask inpainting
python generate_image.py "A sunlit indoor lounge with a pool" --reference ./lounge.png --mask ./mask.png
```

### Output files

Each image is saved with a **metadata JSON sidecar** (`{name}.{ext}.json`) for reproduction and refinement:
```json
{
  "model": "gpt-image-2",
  "prompt": "...",
  "revised_prompt": "...",
  "size": "1024x1024",
  "quality": "high",
  "timestamp": "2026-04-23T10:00:00"
}
```

## Use as a Claude Code skill

### Install into another project

```bash
mkdir -p /path/to/your-project/.claude/skills

ln -s $CCSKILL_GPTIMAGE_DIR/.claude/skills/ccskill-gptimage \
      /path/to/your-project/.claude/skills/ccskill-gptimage
```

Claude Code will auto-discover and use this skill whenever image generation is needed. `git pull` here updates every linked project.

### Skill language

Default is English (`SKILL.md`). To switch to Japanese:

```bash
cd $CCSKILL_GPTIMAGE_DIR/.claude/skills/ccskill-gptimage

mv SKILL.md SKILL.en.md
ln -s SKILL.ja.md SKILL.md
```

## Tests

```bash
source venv/bin/activate
python -m pytest tests/ -v
```

API calls are mocked, so no API key is required to run tests.

## Specs

- **Model**: `gpt-image-2` (snapshot `gpt-image-2-2026-04-21`)
- **Input**: text / images
- **Output**: image only (`b64_json`, no URL is returned)
- **Max resolution**: 2K
- **Endpoints**: `/v1/images/generations`, `/v1/images/edits`
- **Filename**: timestamp form (e.g. `20260423_153045.png`)

## Sister-skill comparison: `ccskill-nanobanana`

| Use case | First choice | Why |
|---|---|---|
| Posters with Japanese/kanji text | **ccskill-gptimage** | Strongest text rendering |
| Business infographics | **ccskill-gptimage** | Agentic reasoning plans structure |
| Editing / partial modification | **ccskill-gptimage** | Always processes input at max fidelity |
| Transparent PNG (logos, icons, sprites) | Either | gpt-image-2 can't, but `--model gpt-image-1.5` can. `rembg` post-processing also works. |
| 4K output | **ccskill-nanobanana** | gpt-image-2 caps at 2K |

## Troubleshooting

| Symptom | Fix |
|---|---|
| `403 Forbidden` | Complete OpenAI Organization Verification |
| `Rate limit exceeded` | Tier 1 is 5 IPM only — production needs Tier 3+ |
| Timeout | Set SDK timeout ≥ 120 s |
| Broken Japanese text | Wrap in `" "`; specify font (`serif Japanese font`) |

## License

MIT
