import gradio as gr
import io
import base64
import ollama

MODEL_NAME = "google/gemma3:4b"


def get_calories(image):
    buffered = io.BytesIO()
    image.save(buffered, format="jpeg")
    base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    prompt = f"- name each food in the image \
    - calculate calorie for each food \
    - calculate total calories \
    - calculate protein for each food \
    - calculate total protein \
    - do not ask for any other information \
    - show results in a table format \
    - display total calories in a table format"
    try:
            
        ollamaClient = ollama.Client(host="http://192.168.1.217:11434")
        response = ollamaClient.chat(
            model="gemma3:4b",
            messages=[
                {"role": "system", "content": "You are an AI assistant that can analyze images and generate 1. what food it contains  2. how many calories in an HTML Table format."},
                {"role": "user", "content": prompt, "images": [base64_image]},
            ]
        )
        if "message" in response:
            return response["message"]["content"]
        else:
            return "Failed to generate caption."
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "Failed to generate caption."
        

# Define the Gradio UI inputs
image_input = gr.Image(type="pil", label="Upload Image")  # 'pil' type for images

# Create the Gradio Interface
gr.Interface(
    fn=get_calories, 
    inputs=[image_input],
    outputs=gr.HTML(label="Calories Information", value="<p>Results will be displayed here</p>"),
    title="Calorie Calculator",
    description="Upload an image of your food and check the calories.",
    allow_flagging="never",
    theme=gr.themes.Ocean
).launch()
