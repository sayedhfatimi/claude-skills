# OpenAI Images API — gpt-image-1.5 Reference

Base URL: `https://api.openai.com/v1/images/generations`

## Request body

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `model` | string | yes | — | Must be `gpt-image-1.5` |
| `prompt` | string | yes | — | Up to ~32,000 chars. Be specific. |
| `n` | integer | no | 1 | 1–10 images |
| `size` | string | no | `1024x1024` | `1024x1024` / `1536x1024` / `1024x1536` |
| `quality` | string | no | `medium` | `low` / `medium` / `high` |
| `output_format` | string | no | `png` | `png` / `jpeg` / `webp` |
| `background` | string | no | `auto` | `transparent` / `opaque` / `auto` — transparent requires png or webp |
| `moderation` | string | no | `auto` | `auto` / `low` — content filtering level |
| `partial_images` | integer | no | — | Stream partial images during generation (0 to disable) |

## Response

```json
{
  "created": 1234567890,
  "data": [
    {
      "b64_json": "<base64-encoded image>",
      "revised_prompt": "The prompt as actually used (may differ from input)"
    }
  ],
  "usage": {
    "input_tokens": 100,
    "output_tokens": 2500,
    "total_tokens": 2600,
    "input_tokens_details": { "text_tokens": 50, "image_tokens": 50 }
  }
}
```

> `gpt-image-1.5` **always returns `b64_json`**, not a URL. You must base64-decode to get the bytes.

## Pricing (approximate — check OpenAI dashboard for current rates)

| Quality | 1024×1024 | 1536×1024 / 1024×1536 |
|---------|-----------|----------------------|
| low | ~$0.011 | ~$0.016 |
| medium | ~$0.042 | ~$0.063 |
| high | ~$0.167 | ~$0.250 |

## Content policy

`gpt-image-1.5` applies OpenAI's usage policies. Requests that violate policy return a 400 with a content moderation reason. Setting `moderation: "low"` relaxes some filters but does not disable them entirely.

## Revised prompt

The API may modify the prompt slightly for safety or quality. The `revised_prompt` field in the response shows what was actually used. Surface this to the user when it differs meaningfully from their input.

## Streaming partial images

Set `partial_images: 3` (or 1–4) to receive progressive image updates during generation. Each partial arrives as a Server-Sent Event. Useful for long high-quality generations. The final event has `"finish_reason": "success"`.

## Error codes

| HTTP | Code | Meaning |
|------|------|---------|
| 400 | `invalid_request_error` | Bad params or content policy violation |
| 401 | `invalid_api_key` | Missing or wrong API key |
| 429 | `rate_limit_exceeded` | Too many requests |
| 500 | `server_error` | OpenAI internal error |

## Image editing (not covered by this skill)

For inpainting / outpainting, use the `/v1/images/edits` endpoint with a mask. That is a separate workflow not in scope for this skill.
