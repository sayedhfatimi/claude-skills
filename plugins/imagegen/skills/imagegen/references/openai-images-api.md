# OpenAI Images API — gpt-image-2.6-sunburst Reference

Base URL: `https://api.openai.com/v1/images/generations`

## Request body

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `model` | string | yes | — | Must be `gpt-image-2.6-sunburst` |
| `prompt` | string | yes | — | Up to ~32,000 chars. Be specific. |
| `n` | integer | no | 1 | 1–10 images |
| `size` | string | no | `1024x1024` | `1024x1024` / `1536x1024` / `1024x1536` |
| `quality` | string | no | `auto` | `low` / `medium` / `high` / `auto` — rendering quality (the script defaults to `medium`) |
| `complexity` | string | no | model default (`high`) | `low` / `medium` / `high` — how much the model plans before rendering; separate from `quality` |
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
      "b64_json": "<base64-encoded image>"
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

> `gpt-image-2.6-sunburst` **always returns `b64_json`**, not a URL. You must base64-decode to get the bytes.

## Pricing

Billed per token (text input, image output), not per image. Check OpenAI's pricing page for current rates.

## Content policy

`gpt-image-2.6-sunburst` applies OpenAI's usage policies. Requests that violate policy return a 400 with a content moderation reason. Setting `moderation: "low"` relaxes some filters but does not disable them entirely.

## Revised prompt

GPT image models do not return `revised_prompt`. Report the prompt you sent.

## Streaming partial images

Set `partial_images` (0–3) with `stream: true` to receive progressive image updates during generation. Each partial arrives as a Server-Sent Event. Useful for long high-quality generations. The final event has `"finish_reason": "success"`.

## Error codes

| HTTP | Code | Meaning |
|------|------|---------|
| 400 | `invalid_request_error` | Bad params or content policy violation |
| 401 | `invalid_api_key` | Missing or wrong API key |
| 429 | `rate_limit_exceeded` | Too many requests |
| 500 | `server_error` | OpenAI internal error |

## Image editing (not covered by this skill)

For inpainting / outpainting, use the `/v1/images/edits` endpoint with a mask. That is a separate workflow not in scope for this skill.
