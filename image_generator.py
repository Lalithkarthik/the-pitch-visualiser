import os
import time
import requests
from urllib.parse import quote
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
POLLINATIONS_API_KEY = os.getenv("POLLINATION_API")
OUTPUT_DIR = "generated_images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Primary - FLUX
client = InferenceClient(
    provider="replicate",
    api_key=HF_TOKEN
)

def clear_generated_images():
    """
    Remove previously generated images.
    """
    for file in os.listdir(OUTPUT_DIR):
        path = os.path.join(OUTPUT_DIR, file)
        if os.path.isfile(path):
            os.remove(path)

def generate_with_flux(prompt):
    """
    Generate image using FLUX via HuggingFace.
    """
    image = client.text_to_image(
        prompt,
        model="black-forest-labs/FLUX.1-dev"
    )
    return image

def generate_with_pollinations(prompt):
    """
    Generate image using Pollinations API.
    """
    encoded_prompt = quote(prompt)
    response = requests.get(
        f"https://gen.pollinations.ai/image/{encoded_prompt}",
        params={"model": "flux"},
        headers={"Authorization": f"Bearer {POLLINATIONS_API_KEY}"},
        timeout=60
    )
    if response.status_code != 200:
        raise Exception("Pollinations generation failed")
    return response.content


def generate_images(prompts):
    """
    Generate storyboard images from prompts.
    Returns list of image paths.
    """
    clear_generated_images()
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    image_paths = []
    for i, prompt in enumerate(prompts):
        print(f"Generating scene {i+1}...")
        filename = f"story_{timestamp}_scene_{i+1}.png"
        destination = os.path.join(OUTPUT_DIR, filename)
        try:
            image = generate_with_flux(prompt)
            image.save(destination)
            print("Generated using FLUX")
        except Exception as e:
            print("FLUX failed, switching to Pollinations:", e)
            try:
                image_bytes = generate_with_pollinations(prompt)
                with open(destination, "wb") as f:
                    f.write(image_bytes)
                print("Generated using Pollinations")
            except Exception as e2:
                print("Pollinations also failed:", e2)
                # If both fail, skip image
                continue

        image_paths.append(destination)
        time.sleep(1) #To avoid hitting API limits

    return image_paths