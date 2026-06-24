import os
import time
from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def call_claude(prompt: str, model: str = "claude-sonnet-4-6") -> dict:
    start = time.time()
    response = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    elapsed = (time.time() - start) * 1000

    return {
        "model_name": model,
        "response": response.content[0].text,
        "latency_ms": round(elapsed, 2)
    }