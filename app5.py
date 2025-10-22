from openai import OpenAI
import config
import sys
import time

openai = OpenAI(api_key=config.OPENAI_API_KEY)

scene1_prompt = """

Scene 1: Morning in the Forest

Setting: A golden sunrise over a forest clearing. Birds sing, leaves rustle, and the air smells of pine and honey.

Main Character: Finn the Fox, clever and fast — but a little too proud.

Plot Point:

Finn loves to race through the forest, showing off his speed.

He teases slower animals — the tortoise, the badger, and even the sleepy owl.

“Catch me if you can!” he laughs, leaving everyone behind.

But when it’s time for lunch or games, no one invites him.

That night, Finn sits alone under the stars, feeling something strange — lonely.

Emotional Tone: Playful at first, then wistful and a little sad.

Illustration Ideas:

Finn leaping joyfully through sun-dappled trees.

Other animals watching with annoyed or hurt faces.

A quiet moment of Finn curled up alone as night falls."""

scene2_prompt = """
Scene 2: The Challenge

Setting: The next day near the riverbank. The current runs fast after a storm.

Plot Point:

Finn hears cries for help — a baby bunny is stuck on a rock in the middle of the rushing water!

The other animals panic but are too scared to help.

Finn hesitates. He’s the fastest and strongest, but he’s never really helped anyone before.

Taking a deep breath, he leaps onto the slippery stones, using his quick feet to reach the bunny.

He brings the bunny safely back to shore. Everyone cheers.

Emotional Tone: Excitement, fear, bravery, relief.

Illustration Ideas:

Splashing water, wind blowing through Finn’s fur.

Finn stretching to grab the bunny’s paw.

A big group of forest animals watching, wide-eyed, from the shore.

Lesson Moment:

The baby bunny says softly, “Thank you, Finn.”

For the first time, Finn feels something better than pride — he feels warm inside."""

scene3_prompt = """Scene 3: A New Day

Setting: The same forest, now bright and friendly.

Plot Point:

The next morning, Finn helps the badger carry berries, waits for the tortoise to cross the path, and shares his favorite sunny spot with the owl.

The animals smile and invite him to play.

They even make him a flower crown that says “Forest Friend.”

Finn realizes that kindness makes the forest — and his heart — much happier than showing off ever did.

Emotional Tone: Joyful, peaceful, full of belonging.

Illustration Ideas:

Finn and his new friends playing together.

A close-up of Finn’s proud-but-gentle smile.

A final wide shot of the forest at sunset, glowing and calm.

Closing Line Options:

From that day on, Finn the Fox was known for his kind heart — and his fastest smile."""

def wait_for_video_completion(video, bar_length=30, poll_interval=2):
    """
    Wait for video generation to complete with progress tracking.
    
    Args:
        video: The video object from OpenAI API
        bar_length: Length of the progress bar (default: 30)
        poll_interval: Time between status checks in seconds (default: 2)
    
    Returns:
        Completed video object
        
    Raises:
        SystemExit: If video generation fails
    """
    progress = getattr(video, "progress", 0)
    
    while video.status in ("in_progress", "queued"):
        # Refresh status
        video = openai.videos.retrieve(video.id)
        progress = getattr(video, "progress", 0)

        filled_length = int((progress / 100) * bar_length)
        bar = "=" * filled_length + "-" * (bar_length - filled_length)
        status_text = "Queued" if video.status == "queued" else "Processing"

        sys.stdout.write(f"\r{status_text}: [{bar}] {progress:.1f}%")
        sys.stdout.flush()
        time.sleep(poll_interval)

    # Move to next line after progress loop
    sys.stdout.write("\n")

    if video.status == "failed":
        message = getattr(
            getattr(video, "error", None), "message", "Video generation failed"
        )
        print(message)
        sys.exit(1)
    
    return video


def download_and_save_video(video, filename):
    """
    Download video content and save it to a file.
    
    Args:
        video: The completed video object from OpenAI API
        filename: The filename to save the video as (e.g., "video1.mp4")
    """
    print(f"Video generation completed: {video}")
    print("Downloading video content...")

    content = openai.videos.download_content(video.id, variant="video")
    content.write_to_file(filename)

    print(f"Wrote {filename}")

# --------------------------------------------------------------
# Create Scene 1
# --------------------------------------------------------------

video1 = openai.videos.create(
    model="sora-2-pro",
    prompt=scene1_prompt,
    size="1280x720",
    seconds="12",
)

video1 = wait_for_video_completion(video1)
download_and_save_video(video1, "storyboard1.mp4")

video2 = openai.videos.remix(
    video_id=video1.id,
    prompt=scene2_prompt,
)

video2 = wait_for_video_completion(video2)
download_and_save_video(video2, "storyboard2.mp4")

# always point at the first video when remixing 
video3 = openai.videos.remix(
    video_id=video1.id,
    prompt=scene3_prompt,
)

video3 = wait_for_video_completion(video3)
download_and_save_video(video3, "storyboard3.mp4")

