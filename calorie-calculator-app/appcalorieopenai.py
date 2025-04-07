import gradio as gr
import io
import base64
import openai


def get_calories(image):
    OPENAI_API_KEY = "<use your own key>"

    buffered = io.BytesIO()
    image.save(buffered, format="jpeg")
    base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    prompt = f"- name each food in the image \
    - calculate calorie for each food \
    - calculate total calories \
    - calculate protein for each food \
    - calculate total protein \
    - do not ask for any other information \
    - show results in a table format"
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant that can analyze images and generate 1. what food it contains  2. how many calories each food in an html table format."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"            

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

