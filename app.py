from openai import OpenAI
import config
import time 

openai = OpenAI(api_key=config.OPENAI_API_KEY)

video = openai.videos.create(
    model="sora-2-pro",
    prompt="A video of a cool cat on a motorcycle in the night",
)

print("Video generation started:", video)
print("Video ID:", video.id)

time.sleep(200)  # This may need to be increased

content = openai.videos.download_content(video.id, variant="video")
content.write_to_file("video.mp4")

print("Wrote video.mp4")


