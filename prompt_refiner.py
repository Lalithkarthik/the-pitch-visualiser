import os
import json
import re
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)


STYLE_MAP = {
    "photorealistic": "photorealistic image, realistic lighting, ultra detailed",
    "digital_art": "digital concept art, vibrant colors, stylized illustration",
    "cinematic": "cinematic movie still, dramatic lighting",
    "watercolor": "watercolor painting, soft brush strokes",
    "comic": "comic book illustration, bold outlines, graphic shading"
}

def generate_story_anchor(scenes):

    try:

        prompt = f"""
Create a concise visual anchor for a storyboard.

Scenes:
{json.dumps(scenes)}

Rules:
- Keep descriptions short (5–10 words each)
- Only describe visible elements
- Avoid narrative or abstract concepts

Return JSON only:

{{
 "characters": "...",
 "environment": "...",
 "camera_style": "...",
 "lighting_style": "..."
}}
"""


        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        match = re.search(r"\{[\s\S]*?\}", text)

        if match:
            anchor = json.loads(match.group())
        else:
            raise ValueError("No JSON object found")

        return anchor

    except Exception as e:

        print("Anchor generation failed:", e)

        return {
            "characters": "diverse startup team and customers",
            "environment": "modern tech startup office",
            "camera_style": "cinematic framing",
            "lighting_style": "dramatic lighting"
        }

def build_flux_prompts(scenes, style="cinematic"):

    anchor = generate_story_anchor(scenes)

    style_prompt = STYLE_MAP.get(style, "")

    prompts = []

    for scene in scenes:

        prompt = (
            f"{style_prompt}, storyboard panel illustration, "
            f"{anchor['environment']}, "
            f"{anchor['characters']}, "
            f"{scene}, "
            f"{anchor['camera_style']}, "
            f"{anchor['lighting_style']}, "
            f"high detail, cinematic composition"
        )

        prompts.append(prompt)

    return prompts
