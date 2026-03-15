import os
import json
import re
from dotenv import load_dotenv
from google import genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

def generate_captions(scenes):
    """
    Generate one concise caption per scene.
    """

    try:

        prompt = f"""
You are writing captions for storyboard panels.

Convert each scene into a short caption.

Rules:
- 1 sentence per caption
- concise and clear
- describe the key action
- present tense
- no quotation marks

Scenes:
{json.dumps(scenes)}

Return ONLY a JSON list of captions.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        text = response.text.strip()
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            captions = json.loads(match.group())
        else:
            raise ValueError("No JSON array found")
        return captions
    except Exception as e:
        print("Caption generation failed:", e)
        # fallback: use scenes directly
        return scenes
