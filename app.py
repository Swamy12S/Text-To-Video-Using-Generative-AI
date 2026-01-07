import os
import json
import argparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# -------- PROJECT IMPORTS --------
from utility.script.script_generator import generate_script
from utility.audio.audio_generator import generate_audio
from utility.captions.timed_captions_generator import generate_timed_captions
from utility.video.background_video_generator import generate_video_url
from utility.video.video_search_query_generator import (
    getVideoSearchQueriesTimed,
    merge_empty_intervals
)
from utility.render.render_engine import get_output_media


# -------- MAIN ENTRY POINT --------
def main():
    parser = argparse.ArgumentParser(description="Generate a short-form video from a topic.")
    parser.add_argument("topic", type=str, help="Topic for the video")

    args = parser.parse_args()
    topic = args.topic

    AUDIO_FILE = "audio_tts.mp3"
    VIDEO_SERVER = "pexel"

    # 1️⃣ Generate Script
    script = generate_script(topic)
    print(f"\n📝 Script Generated:\n{script}\n")

    # 2️⃣ Generate Audio (gTTS – synchronous)
    generate_audio(script, AUDIO_FILE)

    # 3️⃣ Generate Timed Captions (Whisper)
    timed_captions = generate_timed_captions(AUDIO_FILE)
    print("\n🕒 Timed Captions:")
    print(timed_captions)

    # 4️⃣ Generate Video Search Queries
    search_terms = getVideoSearchQueriesTimed(script, timed_captions)
    print("\n🔍 Video Search Queries:")
    print(search_terms)

    if not search_terms:
        print("❌ No search terms generated.")
        return

    # 5️⃣ Fetch Background Videos
    background_video_urls = generate_video_url(search_terms, VIDEO_SERVER)
    background_video_urls = merge_empty_intervals(background_video_urls)

    if not background_video_urls:
        print("❌ No background videos found.")
        return

    # 6️⃣ Render Final Video
    output_video = get_output_media(
        AUDIO_FILE,
        timed_captions,
        background_video_urls,
        VIDEO_SERVER
    )

    print("\n🎬 Final Video Generated:")
    print(output_video)


# -------- RUN --------
if __name__ == "__main__":
    main()
