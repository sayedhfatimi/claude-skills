---
name: imagegen
description: >
  Generate images using OpenAI's gpt-image-1.5 model via the OpenAI Images API.
  Use this skill whenever the user asks to generate, create, draw, render, or
  produce any image — illustrations, concept art, UI mockups, diagrams, icons,
  product visualisations, or any other visual output. Trigger even for casual
  phrasings like "make me a picture of...", "draw...", "visualise...", or
  "create an image of...". Also trigger when the user asks to regenerate or
  refine a previously generated image. Requires OPENAI_API_KEY in the environment.
---

# Image Generation (gpt-image-1.5)

Generate images by calling the OpenAI Images API with the `gpt-image-1.5` model.

## Prerequisites

`OPENAI_API_KEY` is required but **do not check for it yourself** — the script
handles key resolution and will load it automatically from a `.env` file if
present. Just run the script; it will report a clear error if the key truly
cannot be found.

The script looks for the key in this order:
1. `IMAGEGEN_ENV_FILE` env var (explicit path to a `.env` file)
2. `.env` in the current working directory
3. `.env` walking up the directory tree to the project root
4. `~/.env` in the home directory
5. `OPENAI_API_KEY` environment variable

## Workflow

### 1. Clarify the prompt (if needed)

If the user's request is vague or missing important visual detail, ask one concise follow-up question before generating. If the request is clear enough, proceed directly.

Good prompt practices to apply automatically:
- Be specific about style (photorealistic, flat illustration, oil painting, 3D render, pixel art, etc.)
- Include lighting, mood, and composition hints when relevant
- Mention what should NOT appear if the user has exclusions

### 2. Determine output parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| `size` | `1024x1024` | Also supports `1536x1024` (landscape), `1024x1536` (portrait) |
| `quality` | `medium` | `low` / `medium` / `high` — affects detail and credit cost |
| `output_format` | `png` | `png` / `jpeg` / `webp` |
| `n` | `1` | Number of images (1–10) |
| `background` | `auto` | `transparent` (png/webp only) / `opaque` / `auto` |

Choose `landscape` or `portrait` automatically based on the subject when the user doesn't specify. Default to `1024x1024` for ambiguous subjects.

### 3. Generate the image

Use the generation script:

```bash
python scripts/generate.py \
  --prompt "<prompt>" \
  --size 1024x1024 \
  --quality medium \
  --output-dir . \
  [--n 1] \
  [--format png] \
  [--background auto]
```

Or call the API inline if the script isn't available — see **Inline API call** below.

### 4. Report back

After generation, tell the user:
- The output file path(s)
- The final prompt used (so they can iterate)
- Any relevant notes (e.g. if a detail was simplified to fit the model)

---

## Inline API call (Python)

Use this when running without the script, or for quick one-off calls:

```python
import anthropic_imagegen_helper as _  # not real — use the pattern below
```

```python
import os, base64, json, urllib.request

api_key = os.environ["OPENAI_API_KEY"]
prompt  = "A serene Japanese garden at dawn, soft mist, photorealistic"
size    = "1024x1024"
quality = "medium"
fmt     = "png"

payload = json.dumps({
    "model": "gpt-image-1.5",
    "prompt": prompt,
    "n": 1,
    "size": size,
    "quality": quality,
    "output_format": fmt,
}).encode()

req = urllib.request.Request(
    "https://api.openai.com/v1/images/generations",
    data=payload,
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    },
)

with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read())

# gpt-image-1.5 returns b64_json by default
img_bytes = base64.b64decode(data["data"][0]["b64_json"])
out_path   = "output.png"
with open(out_path, "wb") as f:
    f.write(img_bytes)

print(f"Saved: {out_path}")
```

> **Note:** `gpt-image-1.5` always returns `b64_json` (not a URL). Always decode from base64.

---

## Iterative refinement

If the user wants to adjust a generated image:
1. Restate the original prompt with the requested changes
2. Generate again (the model is stateless — there is no inpainting via this skill)
3. For structural changes (crop, composite, resize), use bash/Python image tools (`Pillow`, `ffmpeg`, `convert`) after generation

---

## Error handling

| Error | Likely cause | Fix |
|-------|-------------|-----|
| `401 Unauthorized` | Bad or missing API key | Check `OPENAI_API_KEY` |
| `400 Bad Request` | Invalid param or prompt policy violation | Review prompt and parameters |
| `429 Too Many Requests` | Rate limit | Wait and retry with backoff |
| `billing_hard_limit_reached` | Out of credits | User needs to top up OpenAI account |

---

## Reference

Full API reference: `references/openai-images-api.md`
(Read this file for advanced parameters: `moderation`, `partial_images`, streaming generation.)
