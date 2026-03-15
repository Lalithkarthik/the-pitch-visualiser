# The Pitch Visualizer: From Words to Storyboard

This is an AI-powered tool that converts a written startup story, narrative, or sales pitch into a **visual storyboard**.
The system analyzes narrative text, extracts key scenes, generates visual prompts, and produces images that represent each scene in a cinematic storyboard format.

The goal of the project is to help founders, designers, storytellers and people in general, to **quickly visualize ideas, product journeys, or startup pitches**. This tool would empower people to translate their ideas from just words to a complete visual showcase.

---

# Features

* Converts narrative text into **structured scenes**
* Uses an LLM to **refine scenes into visual descriptions**
* Generates **diffusion-ready prompts** for image generation
* Produces **storyboard images for each scene**
* Automatically generates **captions** for a higher clarity and flow
* Interactive storyboard viewer
* Enables exporting the storyboard as:

  * **PDF**
  * **PowerPoint**

---

# Example Workflow

User Input:

> "A startup struggled with slow customer support. They built an AI assistant that helped customers instantly."

Pipeline Output:

1. Scene segmentation
2. Scene refinement
3. Prompt generation
4. Image generation
5. Storyboard display

Result: A visual storyboard representing the narrative.

---

# Project Architecture

```
User Story (Input text)
     │
     ▼
Story Segmentation (spaCy)
     │
     ▼
Scene Refinement (LLMs)
     │
     ▼
Prompt Engineering (Well-structureed prompt templates)
     │
     ▼
Image Generation (Generative models)
     │
     ▼
Caption Generation (LLMs)
     │
     ▼
Storyboard UI + Export 
```

---

# Project Structure

```
pitch-visualiser/
│
├── app.py
├── segmentation.py
├── scene_refiner.py
├── prompt_refiner.py
├── image_generator.py
├── caption_generator.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── script.js
│   └── style.css
│
├── generated_images/
│
├── requirements.txt
└── README.md
```

---

# Setup Instructions

## 1. Clone the Repository

```
git clone <repository-url>
cd pitch-visualiser
```

---

## 2. Create Virtual Environment

```
python -m venv venv
```

Activate it:

### Mac/Linux

```
source venv/bin/activate
```

### Windows

```
venv\Scripts\activate
```

---

## 3. Install Dependencies

```
pip install -r requirements.txt
```

---

# API Key Configuration

Create a `.env` file in the project root.

Example:

```
GEMINI_API_KEY=your_gemini_api_key
HF_TOKEN=your_huggingface_token
POLLINATION_API=your_pollination_api_key
```

### Required Services

#### Google Gemini API

Used for:

* scene refinement
* story anchors
* caption generation

Can be substituted with other LLMs, but changes should be made in the code accordingly.

Get token from:
https://aistudio.google.com/

---

#### Hugging Face Token (optional)

Used for open-source model inference, used to generate images from the FLUX model. Again, can be replaced with other generative models, but code must be changed accordingly.

Get token from:
https://huggingface.co/settings/tokens

---

#### Pollinations AI (optional)

Used for image generation when the FLUX model accessed from HuggingFace through the HF Token fails, existing as a strong backup, bringing robustness into our image generation task.

Get key from:
https://enter.pollinations.ai/

---

# Running the Application

Start the Flask server:

```
python app.py
```

Then open your browser:

```
http://127.0.0.1:5000
```

Paste a story into the input field and click **Generate Storyboard**.

---

# Prompt Engineering Methodology

Prompt engineering is a key part of this system.
The pipeline separates prompts into two components:

## 1. Global Visual Anchor

The system first generates a **story anchor** that ensures visual consistency across scenes.

Example structure:

```
{
 "characters": "...",
 "environment": "...",
 "camera_style": "...",
 "lighting_style": "..."
}
```

This ensures that:

* characters remain visually consistent
* the environment stays coherent
* cinematic framing remains uniform

---

## 2. Scene Prompts

Each scene is converted into a diffusion-ready prompt using the following structure:

```
STYLE + ENVIRONMENT + CHARACTERS + ACTION + CAMERA + LIGHTING
```

Example:

```
cinematic movie still, dramatic lighting,
modern startup office,
support team overwhelmed by support tickets,
wide shot, shallow depth of field
```

This structure improves:

* prompt clarity
* image quality
* scene consistency

---

# Image Generation Strategy

Instead of generating prompts directly from raw text, the system performs:

```
Story
 → Scene Extraction
 → Scene Refinement
 → Visual Anchor Generation
 → Prompt Construction
```

This layered approach improves the quality and coherence of generated images.

---

# Export Features

Generated storyboards can be exported as:

### PDF

Each panel becomes a page containing:

* image
* caption
* panel number

### PowerPoint

Each scene becomes a slide with:

* full slide image
* caption bar
* panel numbering

---

# Limitations

* Image generation quality depends on the chosen model.
* LLM responses may occasionally require retries.
* Diffusion models may introduce minor visual inconsistencies.

---

# Future Improvements

Potential extensions include:

* consistent character identity across scenes
* animated storyboard generation
* scene editing controls
* multiple visual styles
* real-time image generation

---

# License

This project is intended for research and educational purposes.
