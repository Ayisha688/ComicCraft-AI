import os
import json
from google import genai


def generate_story(
    outline,
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
Create narration, dialogue and captions for this 5-panel comic.

Story prompt: {story_prompt}
Main character: {character_name}
Setting: {setting}
Tone: {tone}
Art style: {art_style}

Comic outline:
{json.dumps(outline, indent=2)}

Return ONLY valid JSON as an array of 5 objects.

Each object must contain:
- panel
- narration
- dialogue
- caption

Keep the text short and suitable for a comic.
"""

    response = client.models.generate_content(
        model=os.getenv("GEMINI_STORY_MODEL", "gemini-3.8-flash"),
        contents=prompt,
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)