import os
import re
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)


def refine_scenes(scenes):
    """
    Refines algorithmically generated scenes using Gemini.
    """

    try: 
        prompt = f"""
You are helping generate a visual storyboard.

You will receive scene fragments extracted from a story.

Tasks:
1. Rewrite them into clear visual storyboard scenes
2. Ensure scenes are concise and visually meaningful
3. Maintain chronological order
4. Return between 3 and 7 scenes
5. Do NOT invent new story elements

IMPORTANT:
Return ONLY a valid JSON array of strings.
Do not include markdown, explanations, or code blocks.

Scenes:
{json.dumps(scenes)}
"""
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        print("RAW MODEL OUTPUT:")
        print(response.text)
        text = response.text.strip()
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if match:
            refined = json.loads(match.group())
        else:
            raise ValueError("No JSON array found in response")
        refined = json.loads(match.group())
        return refined
    except Exception as e:
        print("Gemini failed, using original scenes:", e)
        return scenes

    