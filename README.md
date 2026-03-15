# The Pitch Visualizer: From Words to Storyboard

This is an AI-powered tool that converts a written startup story, narrative, or sales pitch into a **visual storyboard**.
The system analyzes narrative text, extracts key scenes, generates visual prompts, and produces images that represent each scene in a cinematic storyboard format.

The goal of the project is to help founders, designers, storytellers and people in general, to **quickly visualize ideas, product journeys, or startup pitches**. This tool would empower people to translate their ideas from just words to a complete visual showcase.

Demo Video: https://drive.google.com/file/d/147Coc9346jvWWeoiu_jsRXSJCZhPGrok/view?usp=sharing

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
git clone https://github.com/Lalithkarthik/the-pitch-visualiser.git
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

# System Methodology

The Pitch Visualizer uses a **multi-stage AI pipeline** to convert narrative text into a structured visual storyboard.
Rather than directly generating images from the raw input text, the system decomposes the task into several stages that progressively transform the input into more structured and visually meaningful representations.

This design improves:

* scene clarity
* prompt quality
* visual consistency across generated images

The pipeline follows the architecture below:

```
Story Text
   ↓
Scene Segmentation
   ↓
Scene Refinement
   ↓
Visual Anchor Generation
   ↓
Prompt Engineering
   ↓
Image Generation
   ↓
Caption Generation
```

Each stage is designed to solve a specific challenge involved in translating **natural language narratives into visual scenes**.

---

# 1. Story Segmentation

Narrative text typically contains multiple events within a single paragraph.
If this text is sent directly to an image generation model, the model may attempt to visualize **several unrelated events simultaneously**, leading to cluttered or ambiguous images.

To address this issue, the system first performs **story segmentation**.

Using the **spaCy NLP library**, the input text is analyzed and broken down into **smaller narrative fragments representing individual events or scenes**.

Example input:

```
A startup struggled with slow customer support.
They built an AI assistant that solved the problem.
Soon customers were happier.
```

Segmented scenes:

```
Scene 1: Startup struggles with slow support
Scene 2: Team builds AI assistant
Scene 3: Customers receive instant help
```

### Justification

Segmentation improves the pipeline by ensuring that:

* each image corresponds to **one clear event**
* prompts remain **short and visually focused**
* storyboard panels maintain **chronological order**

Without this step, diffusion models may produce images that attempt to represent **multiple parts of the story at once**, reducing visual clarity.

---

# 2. Scene Refinement

The segmented scenes are often **too abstract or incomplete** to produce meaningful images.

For example:

```
Startup struggles with support
```

This statement does not specify:

* the environment
* the characters
* the visible actions

To enrich these descriptions, the system performs **scene refinement using a Large Language Model (LLM)**.

The LLM rewrites each scene into a **clear visual description** while maintaining the original narrative meaning.

Example transformation:

Input scene:

```
Startup struggles with support
```

Refined scene:

```
A small startup support team looks overwhelmed as customer tickets pile up across multiple monitors.
```

### Justification

LLMs are particularly effective at converting **abstract narrative statements into concrete visual descriptions**.

This step ensures that prompts contain:

* visible objects
* identifiable characters
* clear actions

These elements significantly improve the performance of image generation models.

---

# Prompt Engineering Methodology

Prompt engineering is a key component of this system.
Rather than sending raw descriptions directly to image models, the system constructs **structured prompts designed to improve generation quality and consistency**.

The prompt engineering strategy is divided into two major components.

---

## 1. Global Visual Anchor

One of the main challenges in generating multi-scene storyboards is **visual consistency across scenes**.

If prompts are generated independently for each scene, image models may produce:

* different character appearances
* inconsistent environments
* varying visual styles

To address this, the system first generates a **global visual anchor**.

The anchor describes the shared visual characteristics of the story, including:

```
{
 "characters": "...",
 "environment": "...",
 "camera_style": "...",
 "lighting_style": "..."
}
```

Example anchor:

```
{
 "characters": "young startup engineers and support agents",
 "environment": "modern open-plan tech startup office",
 "camera_style": "cinematic framing with wide and close-up shots",
 "lighting_style": "dramatic soft lighting"
}
```

This anchor is generated once and reused when constructing prompts for each scene.

### Justification

The visual anchor ensures that:

* characters remain visually recognizable
* environments stay consistent
* scenes appear to belong to the same story world

Without this step, the storyboard may look like **a collection of unrelated images rather than a coherent narrative sequence**.

---

## 2. Scene Prompt Construction

Once the global anchor is established, each refined scene is converted into a **diffusion-ready prompt**.

The system uses a structured template that organizes prompt components in a specific order:

```
STYLE + ENVIRONMENT + CHARACTERS + ACTION + CAMERA + LIGHTING
```

Example prompt:

```
cinematic movie still, dramatic lighting,
modern startup office environment,
support team overwhelmed by customer tickets,
wide shot, shallow depth of field
```

### Justification

This structured approach aligns with how diffusion models interpret prompts.

Each component plays a specific role:

**Style tokens**

Control artistic direction and visual aesthetics.

Example:

```
cinematic movie still
digital concept art
watercolor illustration
```

---

**Environment tokens**

Establish the physical context of the scene.

Example:

```
modern startup office
busy warehouse
city street at night
```

---

**Character tokens**

Ensure that the same characters appear consistently across scenes.

Example:

```
startup engineers and support agents
```

---

**Action tokens**

Describe the primary event occurring in the scene.

Example:

```
support team overwhelmed by tickets
engineers deploying an AI assistant
```

---

**Camera tokens**

Improve scene composition by specifying framing.

Example:

```
wide shot
close-up
over-the-shoulder shot
```

---

**Lighting tokens**

Enhance visual realism and cinematic quality.

Example:

```
dramatic lighting
soft studio lighting
golden hour light
```

---

This prompt structure ensures that each generated image contains:

* clear subject focus
* consistent environment
* coherent visual composition

---

# 5. Image Generation

The structured prompts are then passed to an image generation model.

The system supports multiple image generation backends, including:

* open-source diffusion models
* hosted inference APIs
* alternative generative image services

Each prompt produces a **single storyboard panel**.

### Justification

Using generative image models allows the system to:

* dynamically create visuals for arbitrary stories
* maintain stylistic coherence across panels
* generate storyboards quickly without manual illustration.

---

# 6. Caption Generation

After images are generated, the system produces **captions for each scene using an LLM**.

These captions summarize the narrative context of the image.

Example:

```
Scene: Support agents overwhelmed by tickets

Caption:
"Customer support demand grows rapidly as the startup struggles to keep up."
```

### Justification

Captions improve the storyboard by:

* reinforcing narrative flow
* clarifying scene interpretation
* improving presentation readability

They are especially useful when exporting storyboards to **PDF or PowerPoint formats**.

---

# Design Philosophy

The system follows three guiding design principles.

### Modular Pipeline

Each stage performs a specific transformation, allowing components to be improved or replaced independently.

---

### LLM + Diffusion Collaboration

The system combines two complementary AI capabilities.

LLMs provide:

* reasoning
* narrative interpretation
* prompt generation

Diffusion models provide:

* visual rendering
* scene composition
* stylistic imagery

Together, they produce more coherent storyboards than either model type alone.

---

### Structured Prompts Over Long Prompts

Rather than using extremely long prompts, the system relies on **structured prompts with clearly defined semantic components**.

This results in:

* improved image generation quality
* reduced prompt ambiguity
* better scene consistency.

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
* Currently we rely on at least one of FLUX or POLLINATIONS to work to obtain our images, and failure in both would result in the collapse of our project.

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
