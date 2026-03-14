import os
import time
import random
import shutil

OUTPUT_DIR = "generated_images"
SOURCE_DIR = "static/demo_images"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def clear_generated_images():

    for file in os.listdir(OUTPUT_DIR):

        path = os.path.join(OUTPUT_DIR, file)

        if os.path.isfile(path):
            os.remove(path)


def generate_images(prompts):
    """
    Temporary image generator using random static images.
    """

    clear_generated_images()

    timestamp = time.strftime("%Y%m%d_%H%M%S")

    image_paths = []

    demo_images = os.listdir(SOURCE_DIR)

    for i, prompt in enumerate(prompts):

        filename = f"story_{timestamp}_scene_{i+1}.png"

        source = os.path.join(SOURCE_DIR, random.choice(demo_images))

        destination = os.path.join(OUTPUT_DIR, filename)

        shutil.copy(source, destination)

        image_paths.append(destination)

    return image_paths