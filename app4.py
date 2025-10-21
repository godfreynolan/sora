from openai import OpenAI
import config
import time 
import sys

openai = OpenAI(api_key=config.OPENAI_API_KEY)

basic_prompt = "A cheerful family picnic in a sunny park. Parents set up a blanket under a big oak tree while kids fly kites and toss a frisbee. The camera pans over sandwiches, lemonade, and a puppy chasing bubbles. Gentle acoustic music plays as everyone laughs and enjoys the afternoon."
remix_prompt = "The scene shifts to a close-up of the family dog catching a frisbee mid-air, then zooms out to show the whole family playing together, with the sun setting in the background, casting a warm golden glow over the park."

# create basic video
video = openai.videos.create(
    model="sora-2-pro",
    prompt=basic_prompt,
)

print("Video generation started:", video)
print("Video ID:", video.id)

time.sleep(400)  # This may need to be increased

content = openai.videos.download_content(video.id, variant="video")
content.write_to_file("video1.mp4")

print("Wrote video1.mp4")

# create remixed video
remix_video = openai.videos.remix(
    video_id=video.id,
    prompt=remix_prompt,
)

print("Video 2 generation started:", remix_video)
print("Video ID:", remix_video.id)

time.sleep(400)  # This may need to be increased


print("Video generation completed:", remix_video)
print("Downloading video content...")

content = openai.videos.download_content(remix_video.id, variant="video")
content.write_to_file("video2.mp4")

print("Wrote video2.mp4")
