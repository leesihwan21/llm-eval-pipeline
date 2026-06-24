from app.services.llm_client import call_claude

def evaluate_response(prompt: str, response: str) -> float:
    eval_prompt = f"""아래 질문과 답변을 평가해주세요.

질문: {prompt}
답변: {response}

다음 기준으로 0.0 ~ 1.0 사이 점수만 숫자로 답하세요:
- 정확성
- 완성도
- 자연스러움

점수만 출력 (예: 0.85)"""

    result = call_claude(eval_prompt)
    try:
        score = float(result["response"].strip())
        return round(score, 2)
    except:
        return 0.5