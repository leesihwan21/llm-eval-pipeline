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
    
import os
import time
from dotenv import load_dotenv
import anthropic
from openai import OpenAI
import google.generativeai as genai

load_dotenv()

anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

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

def call_gemini(prompt: str, model: str = "gemini-1.5-flash") -> dict:
    start = time.time()
    gemini_model = genai.GenerativeModel(model)
    response = gemini_model.generate_content(prompt)
    elapsed = (time.time() - start) * 1000
    return {
        "model_name": model,
        "response": response.text,
        "latency_ms": round(elapsed, 2)
    }

def call_llm(prompt: str, model: str) -> dict:
    if "claude" in model:
        return call_claude(prompt, model)
    elif "gpt" in model:
        return call_openai(prompt, model)
    elif "gemini" in model:
        return call_gemini(prompt, model)
    else:
        raise ValueError(f"지원하지 않는 모델: {model}")