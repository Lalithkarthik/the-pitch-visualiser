from flask import Flask, render_template, request, jsonify, send_from_directory

from segmentation import segment_story
from scene_refiner import refine_scenes
from prompt_refiner import build_flux_prompts
from image_generator import generate_images
from caption_generator import generate_captions

app = Flask(__name__, static_folder="static")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():

    data = request.json
    text = data.get("text")
    style = data.get("style")
    
    # segmentation
    scenes = segment_story(text)
    print("Segmented scenes:", scenes)

    # scene refinement
    refined_scenes = refine_scenes(scenes)
    print("Refined scenes:", refined_scenes)

    # prompt generation
    prompts = build_flux_prompts(refined_scenes, style)
    print("Prompts generated")

    # image generation
    image_paths = generate_images(prompts)
    print("Images generated:", image_paths)

    # captions
    captions = generate_captions(refined_scenes)
    print("Captions generated")

    return jsonify({
        "images": image_paths,
        "captions": captions
    })


@app.route("/generated_images/<filename>")
def generated_images(filename):
    return send_from_directory("generated_images", filename)


if __name__ == "__main__":
    app.run(debug=True)
