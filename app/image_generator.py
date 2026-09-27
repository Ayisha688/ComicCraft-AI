import os
import re
from pathlib import Path

import torch
from diffusers import StableDiffusionPipeline

OUTPUT_DIR = Path("static/panels")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL_ID = os.getenv(
    "SD_MODEL",
    "runwayml/stable-diffusion-v1-5",
)

_pipe = None


def get_pipeline():
    global _pipe
    if _pipe is not None:
        return _pipe

    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.float32

    _pipe = StableDiffusionPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=dtype,
        use_safetensors=True,
    )
    _pipe = _pipe.to(device)

    if device == "cpu":
        _pipe.enable_attention_slicing()

    return _pipe


def generate_image(prompt: str, art_style: str = "comic book"):
    pipe = get_pipeline()

    safe = re.sub(r"[^a-zA-Z0-9_-]+", "_", prompt)[:60].strip("_")
    if not safe:
        safe = "panel"

    filename = f"{safe}_{abs(hash(prompt)) % 100000}.png"
    output_path = OUTPUT_DIR / filename

    full_prompt = (
        f"{prompt}, {art_style} style, comic panel, expressive characters, "
        "clear composition, detailed background, vibrant illustration"
    )

    image = pipe(
        full_prompt,
        num_inference_steps=20,
        guidance_scale=7.5,
    ).images[0]

    image.save(output_path)
    return f"/static/panels/{filename}"
