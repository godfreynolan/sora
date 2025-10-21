import time
from openai import OpenAI
from pathlib import Path
import base64
from utils.resizer import resize_image
import config
import sys

openai = OpenAI(api_key=config.OPENAI_API_KEY)

# generate reference image
response = openai.responses.create(
    model="gpt-5",
    input="A portrait photo of a siamese cat wearing steampunk goggles and a leather aviator hat, high detail, dramatic lighting",
    tools=[
        {
            "type": "image_generation",
            "size": "1024x1536",
            "quality": "high",
        }
    ],
)

image_data = [
    output.result
    for output in response.output
    if output.type == "image_generation_call"
]

if image_data:
    image_base64 = image_data[0]

    with open("siamese.png", "wb") as f:
        f.write(base64.b64decode(image_base64))
    resize_image("siamese.png")
    print("Saved and resized image to 720x1280")

video = openai.videos.create(
    model="sora-2",
    prompt="The cat turns around and then walks out of the frame.",
    input_reference=("siamese.png"),
    size="720x1280",
    seconds=4,
)

print("Video generation started:", video)
print("Video ID:", video.id)

time.sleep(600)  # This may need to be increased

content = openai.videos.download_content(video.id, variant="video")
content.write_to_file("siamese.mp4")

print("Wrote siamese.mp4")

