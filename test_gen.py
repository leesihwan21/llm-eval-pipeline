import os
import json
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

prompt = """AI 챗봇의 좋은 응답 예시 5개를 JSON 배열로 생성해주세요.
순수 JSON만 출력하세요:
[{"text": "응답 내용", "label": 1}]"""

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1000,
    messages=[{"role": "user", "content": prompt}]
)

print(response.content[0].text)