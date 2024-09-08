import gradio as gr
from pyngrok import ngrok
import requests


def call_vehicle_count_api(video_path):

    with open(video_path, "rb") as file:
        files = {'file': ('video.mp4', file, 'video/mp4')}
        response = requests.post("http://localhost:8002/count_vehicles/", files=files)

    if response.status_code == 200:
        result = response.json().get("vehicle_count", "Error counting vehicles")
    else:
        result = "API call failed"

    return result


with gr.Blocks() as demo:
    gr.Markdown("### Vehicle Counting Application")
    video_input = gr.Video(label="Upload Video")
    result_output = gr.Textbox(label="Vehicle Count Result")
    submit_btn = gr.Button("Count Vehicles")
    submit_btn.click(fn=call_vehicle_count_api, inputs=video_input, outputs=result_output)

# Setup ngrok tunnel
ngrok.set_auth_token("2lkg7cF6K9CPabEYd2bsfEsLDjm_RAXrdH6NgztakaVxh5PN")
public_url = ngrok.connect(7861)
print("Public URL:", public_url)

# Launch the Gradio app locally
demo.launch()









