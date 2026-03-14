# from segmentation import segment_story
# from scene_refiner import refine_scenes
# from prompt_refiner import build_flux_prompts

# text = """
# A small startup built a productivity tool, but users struggled to understand how to use it. The support inbox kept filling up with the same basic questions every day. The small support team tried their best to respond, but the backlog kept growing and customers were getting frustrated. During a team meeting, someone suggested using AI to automatically answer common questions. The engineers built and deployed an AI assistant connected to the support system. Soon customers started receiving instant replies and the support team finally had time to focus on harder problems. As response times dropped and satisfaction improved, the startup began to grow quickly.
# """

# scenes = segment_story(text)

# for i, scene in enumerate(scenes):
#     print(f"Scene {i+1}: {scene}")

# refined_scenes = refine_scenes(scenes)
# prompts = build_flux_prompts(refined_scenes)
# print(prompts)


# #Image generation using FLUX
# import os
# from dotenv import load_dotenv
# from huggingface_hub import InferenceClient
# load_dotenv()
# client = InferenceClient(
#     provider="replicate",
#     api_key=os.getenv("HF_TOKEN"),
# )
# # output is a PIL.Image object
# image = client.text_to_image(
#     "Astronaut riding a horse",
#     model="black-forest-labs/FLUX.1-dev",
# )
# image.save('new_image_file.jpg') #WORKS!


#Testing image generation alone
# prompts = ['comic movie still, dramatic lighting, storyboard panel illustration, Modern startup office, desks, computers, screens, whiteboard., Startup employees: varied expressions (confused, overwhelmed, relieved)., A small startup office. A screen displays a complex productivity tool, with users looking confused., Mix of close-ups, mid-shots, wide shots, mostly eye-level., Functional office lighting, screen glow, transitioning to brighter., high detail, comic composition', 'comic movie still, dramatic lighting, storyboard panel illustration, Modern startup office, desks, computers, screens, whiteboard., Startup employees: varied expressions (confused, overwhelmed, relieved)., An overwhelmed support team member stares at an email inbox overflowing with repetitive basic questions., Mix of close-ups, mid-shots, wide shots, mostly eye-level., Functional office lighting, screen glow, transitioning to brighter., high detail, comic composition', "comic movie still, dramatic lighting, storyboard panel illustration, Modern startup office, desks, computers, screens, whiteboard., Startup employees: varied expressions (confused, overwhelmed, relieved)., During a team meeting, someone points to a whiteboard, suggesting 'AI' for automatic answers., Mix of close-ups, mid-shots, wide shots, mostly eye-level., Functional office lighting, screen glow, transitioning to brighter., high detail, comic composition", "comic movie still, dramatic lighting, storyboard panel illustration, Modern startup office, desks, computers, screens, whiteboard., Startup employees: varied expressions (confused, overwhelmed, relieved)., Engineers are seen coding and deploying an 'AI Assistant' system, connecting it to the support platform., Mix of close-ups, mid-shots, wide shots, mostly eye-level., Functional office lighting, screen glow, transitioning to brighter., high detail, comic composition", 'comic movie still, dramatic lighting, storyboard panel illustration, Modern startup office, desks, computers, screens, whiteboard., Startup employees: varied expressions (confused, overwhelmed, relieved)., Customers receive instant, helpful replies. The support team is now focused on complex problems, looking relieved., Mix of close-ups, mid-shots, wide shots, mostly eye-level., Functional office lighting, screen glow, transitioning to brighter., high detail, comic composition', 'comic movie still, dramatic lighting, storyboard panel illustration, Modern startup office, desks, computers, screens, whiteboard., Startup employees: varied expressions (confused, overwhelmed, relieved)., Charts illustrate rapidly increasing customer satisfaction and significant startup growth., Mix of close-ups, mid-shots, wide shots, mostly eye-level., Functional office lighting, screen glow, transitioning to brighter., high detail, comic composition']
# from image_generator import generate_images
# paths = generate_images(prompts)

# print(paths)

from together import Together

client = Together()
response = client.images.generate(
    prompt="Cats eating popcorn",
    model="black-forest-labs/FLUX.1-schnell-Free"
)
print(response.data[0].b64_json)