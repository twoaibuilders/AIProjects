import gradio as gr
from PIL import Image
import io
import base64
import ollama

MODEL_NAME = "google/gemma3:4b"


def get_caption(image, caption_mood, occasion, max_words):

    buffered = io.BytesIO()
    image.save(buffered, format="jpeg")
    base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    prompt = f"- maximum length of {max_words} words \
    - caption mood: {caption_mood} \
    - the occasion is {occasion} \
    - do not make this as a quote from the person in the image"
    try:
        response = ollama.chat(model="gemma3:4b", messages=[
            {"role": "system", "content": "You are an AI assistant can analyze image and generate 1. captions and 2. five social media hashtags seperated by comma."},
            {"role": "user", "content": prompt , "images": [base64_image]},  
        ])

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
    
    if "message" in response:
        return response["message"]["content"]
    else:
        return "Failed to generate caption."

# Define the Gradio UI inputs
image_input = gr.Image(type="pil", label="Upload Image")  # 'pil' type for images
mood_input = gr.Dropdown(choices=["Random", "Happy", "Excited", "Motivated", "Relaxed", "Sad", "Adventurous", "Confident", "Grateful", "Inspirational", "Serene"], label="Caption Mood")
occasion_input = gr.Dropdown(choices=["Random", "Birthday", "Graduation", "Wedding", "Anniversary", "Weekend Getaway", "New Job", "Holiday", "Success", "Christmas", "New Year"], label="Occasion")
max_words_input = gr.Slider(minimum=1, maximum=20,step=1 , label="Max Caption Length (Words)")

# Create the Gradio Interface
gr.Interface(
    fn=get_caption, 
    inputs=[image_input, mood_input, occasion_input, max_words_input],
    outputs="text",
    title="Image Caption Generator",
    description="Upload an image and provide details to generate a caption for it.",
    allow_flagging="never",
    theme="citrus"
).launch()
