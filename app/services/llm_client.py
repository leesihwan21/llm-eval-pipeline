import os
import time
from dotenv import load_dotenv
import anthropic
from openai import OpenAI

load_dotenv()

anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_claude(prompt: str, model: str = "claude-sonnet-4-6") -> dict:
    start = time.time()
    response = anthropic_client.messages.create(
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

def call_openai(prompt: str, model: str = "gpt-4o-mini") -> dict:
    start = time.time()
    response = openai_client.chat.completions.create(
        model=model,
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    elapsed = (time.time() - start) * 1000
    return {
        "model_name": model,
        "response": response.choices[0].message.content,
        "latency_ms": round(elapsed, 2)
    }

def call_llm(prompt: str, model: str) -> dict:
    if "claude" in model:
        return call_claude(prompt, model)
    elif "gpt" in model:
        return call_openai(prompt, model)
    else:
        raise ValueError(f"지원하지 않는 모델: {model}")