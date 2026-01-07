import os
import json

# ---------- SAFE ENV LOADING ----------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = None
model = None

# ---------- CLIENT SELECTION ----------
if GROQ_API_KEY and len(GROQ_API_KEY) > 30:
    from groq import Groq
    client = Groq(api_key=GROQ_API_KEY)
    model = "llama-3.1-8b-instant"


elif OPENAI_API_KEY and len(OPENAI_API_KEY) > 30:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
    model = "gpt-4o"

else:
    raise EnvironmentError(
        "No valid API key found. Please set GROQ_API_KEY or OPENAI_API_KEY."
    )


# ---------- SCRIPT GENERATOR ----------
def generate_script(topic: str) -> str:
    prompt = """
You are a seasoned content writer for YouTube Shorts, specializing in FACTS videos.

Rules:
- Duration under 50 seconds (~140 words max)
- Very engaging, punchy, and original
- Output ONLY valid JSON
- JSON must contain ONE key: "script"

Example output:
{"script": "Weird facts you didn't know..."}
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": topic}
        ],
        temperature=0.7
    )

    content = response.choices[0].message.content.strip()

    # ---------- SAFE JSON PARSING ----------
    try:
        data = json.loads(content)
        return data["script"]

    except json.JSONDecodeError:
        # fallback extraction
        start = content.find("{")
        end = content.rfind("}") + 1
        if start == -1 or end == -1:
            raise ValueError("Model did not return valid JSON")

        cleaned = content[start:end]
        data = json.loads(cleaned)
        return data["script"]
