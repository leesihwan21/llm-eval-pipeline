import os
import json
import time
import random
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

topics = [
    "파이썬", "머신러닝", "딥러닝", "RAG", "Docker", "FastAPI",
    "LLM", "자연어처리", "데이터베이스", "클라우드", "API",
    "Git", "CI/CD", "알고리즘", "자료구조", "웹개발",
    "보안", "네트워크", "운영체제", "객체지향"
]

def generate_single(label):
    topic = random.choice(topics)
    
    if label == 1:
        prompt = f"'{topic}'에 대한 AI 챗봇의 좋은 응답 예시 1개를 만들어주세요. 정확하고 구체적이며 2-3문장으로 작성하세요. 순수 JSON만 출력:\n{{\"text\": \"응답내용\", \"label\": 1}}"
    else:
        prompt = f"'{topic}'에 대한 AI 챗봇의 나쁜 응답 예시 1개를 만들어주세요. 모호하거나 도움이 안되는 1문장으로 작성하세요. 순수 JSON만 출력:\n{{\"text\": \"응답내용\", \"label\": 0}}"

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    text = response.content[0].text
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()
    return json.loads(text.strip())

if __name__ == "__main__":
    all_data = []

    # 좋은 응답 200개
    for i in range(200):
        try:
            data = generate_single(label=1)
            all_data.append(data)
            if (i+1) % 20 == 0:
                print(f"Good {i+1}/200 완료")
        except Exception as e:
            print(f"Good Error {i+1}: {e}")
        time.sleep(0.3)

    print(f"좋은 응답 생성: {len([d for d in all_data if d['label']==1])}개")

    with open("synthetic_data_v2.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    print(f"Total: {len(all_data)} saved -> synthetic_data_v2.json")