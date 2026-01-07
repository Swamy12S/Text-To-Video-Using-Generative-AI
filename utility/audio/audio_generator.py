from gtts import gTTS
# Utility to generate audio from text using gTTS
def generate_audio(text: str, output_filename: str):
    """
    Generate audio from text using Google Text-to-Speech (gTTS).
    Stable replacement for edge-tts.
    """
    tts = gTTS(text=text, lang="en")
    tts.save(output_filename)

    print(f"Audio generated successfully: {output_filename}")

     



