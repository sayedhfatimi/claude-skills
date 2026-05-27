#!/usr/bin/env python3
"""
imagegen/scripts/generate.py
Generate images via OpenAI gpt-image-1.5 and save to disk.
"""

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path


def load_env_file(env_path: Path) -> None:
    """Parse a .env file and set variables into os.environ (won't overwrite existing vars)."""
    if not env_path.is_file():
        return
    with env_path.open() as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def find_and_load_env() -> None:
    """
    Look for a .env file in order:
      1. Path in IMAGEGEN_ENV_FILE env var (explicit override)
      2. Current working directory (.env)
      3. Project root — walk up from cwd until .git or filesystem root
      4. Home directory (~/.env)
    """
    # 1. Explicit override
    explicit = os.environ.get("IMAGEGEN_ENV_FILE")
    if explicit:
        load_env_file(Path(explicit))
        return

    # 2. Current working directory
    cwd_env = Path.cwd() / ".env"
    if cwd_env.is_file():
        load_env_file(cwd_env)
        return

    # 3. Walk up to project root (stops at .git or filesystem root)
    current = Path.cwd()
    while True:
        candidate = current / ".env"
        if candidate.is_file():
            load_env_file(candidate)
            return
        if (current / ".git").exists() or current.parent == current:
            break
        current = current.parent

    # 4. Home directory fallback
    load_env_file(Path.home() / ".env")


def parse_args():
    p = argparse.ArgumentParser(description="Generate images with gpt-image-1.5")
    p.add_argument("--prompt", required=True, help="Image generation prompt")
    p.add_argument(
        "--size",
        default="1024x1024",
        choices=["1024x1024", "1536x1024", "1024x1536"],
        help="Image dimensions",
    )
    p.add_argument(
        "--quality",
        default="medium",
        choices=["low", "medium", "high"],
        help="Generation quality (affects cost)",
    )
    p.add_argument(
        "--format",
        default="png",
        choices=["png", "jpeg", "webp"],
        dest="fmt",
        help="Output image format",
    )
    p.add_argument(
        "--background",
        default="auto",
        choices=["auto", "transparent", "opaque"],
        help="Background transparency (transparent only works with png/webp)",
    )
    p.add_argument("--n", type=int, default=1, help="Number of images to generate (1-10)")
    p.add_argument(
        "--output-dir",
        default=".",
        help="Directory to save generated images",
    )
    p.add_argument(
        "--output-name",
        default=None,
        help="Base filename (without extension). Defaults to timestamped name.",
    )
    return p.parse_args()


def generate(args) -> list[str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print(
            "ERROR: OPENAI_API_KEY not found.\n"
            "Set it in your environment, or add it to a .env file in your project root or home directory:\n"
            "  OPENAI_API_KEY=sk-...",
            file=sys.stderr,
        )
        sys.exit(1)

    payload = {
        "model": "gpt-image-1.5",
        "prompt": args.prompt,
        "n": args.n,
        "size": args.size,
        "quality": args.quality,
        "output_format": args.fmt,
    }

    if args.background != "auto":
        payload["background"] = args.background

    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        print(f"ERROR {e.code}: {body}", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    saved = []

    for i, item in enumerate(data.get("data", [])):
        b64 = item.get("b64_json")
        if not b64:
            print(f"WARNING: No b64_json in item {i}", file=sys.stderr)
            continue

        img_bytes = base64.b64decode(b64)

        if args.output_name:
            stem = args.output_name if args.n == 1 else f"{args.output_name}_{i+1}"
        else:
            stem = f"imagegen_{timestamp}" if args.n == 1 else f"imagegen_{timestamp}_{i+1}"

        out_path = out_dir / f"{stem}.{args.fmt}"
        out_path.write_bytes(img_bytes)
        saved.append(str(out_path))
        print(f"Saved: {out_path}")

    return saved


def main():
    find_and_load_env()
    args = parse_args()
    paths = generate(args)
    if not paths:
        print("No images were saved.", file=sys.stderr)
        sys.exit(1)
    # Print all paths as JSON for easy parsing by Claude
    print(json.dumps({"saved": paths}))


if __name__ == "__main__":
    main()
