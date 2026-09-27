import os
import json
from google import genai


def generate_outline(
    story_prompt,
    character_name,
    setting,
    tone,
    art_style
):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to your .env file."
        )

    client = genai.Client(api_key=api_key)

    prompt = f"""
Create a 5-panel comic story outline.

Story prompt: {story_prompt}
Main character: {character_name}
Setting: {setting}
Tone: {tone}
Art style: {art_style}

Return ONLY valid JSON in this format:

[
  {{
    "panel": 1,
    "title": "Panel title",
    "scene_description": "Scene description",
    "image_prompt": "Detailed image generation prompt"
  }}
]

Create exactly 5 panels.
"""

    response = client.models.generate_content(
        model=os.getenv("GEMINI_FLASH_MODEL", "gemini-3.8-flash"),
        contents=prompt,
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)