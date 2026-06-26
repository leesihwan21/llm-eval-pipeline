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
    
import re
from rouge_score import rouge_scorer
from app.services.llm_client import call_claude

def compute_rouge(reference: str, hypothesis: str) -> dict:
    """ROUGE-1, ROUGE-2, ROUGE-L F1 점수 계산"""
    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    scores = scorer.score(reference, hypothesis)
    return {
        "rouge1": round(scores["rouge1"].fmeasure, 4),
        "rouge2": round(scores["rouge2"].fmeasure, 4),
        "rougeL": round(scores["rougeL"].fmeasure, 4),
    }

def evaluate_response(prompt: str, response: str) -> dict:
    """
    LLM-as-a-Judge + ROUGE 복합 평가
    Returns: {llm_score, rouge1, rouge2, rougeL}
    """
    eval_prompt = f"""다음 지시문과 응답을 평가해주세요.

지시문: {prompt}
응답: {response}

다음 기준으로 0.0 ~ 1.0 사이 소수점 점수만 출력하세요:
- 정확성
- 완성도
- 자연스러움

점수만 출력 (예: 0.85)"""

    result = call_claude(eval_prompt)
    try:
        llm_score = float(re.search(r"\d+\.\d+", result["response"]).group())
        llm_score = round(min(max(llm_score, 0.0), 1.0), 2)
    except:
        llm_score = 0.5

    rouge = compute_rouge(reference=prompt, hypothesis=response)

    return {
        "llm_score": llm_score,
        "rouge1": rouge["rouge1"],
        "rouge2": rouge["rouge2"],
        "rougeL": rouge["rougeL"],
    }