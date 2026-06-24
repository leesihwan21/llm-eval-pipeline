# 🧪 LLM Eval Pipeline

LLM 응답 품질 자동 평가 파이프라인 | FastAPI + React + Hugging Face Fine-tuning

## 📌 프로젝트 개요

다양한 LLM(Claude, GPT)의 응답 품질을 자동으로 평가하고 비교하는 풀스택 AI 서비스입니다.
LLM-as-a-Judge 방식과 직접 fine-tuning한 분류 모델을 활용하여 응답 품질을 평가합니다.

## 🛠 기술 스택

**Backend:** FastAPI, SQLAlchemy, SQLite
**Frontend:** React, Vite, Tailwind CSS, Recharts
**AI/ML:** Anthropic Claude, OpenAI GPT-4o Mini, Hugging Face (klue/roberta-base)
**Infra:** Docker, GitHub Actions CI/CD, AWS EC2 (예정)

## ✨ 주요 기능

- 멀티 LLM 응답 생성 및 비교 (Claude Sonnet, GPT-4o Mini)
- LLM-as-a-Judge 자동 품질 평가 (0~1점)
- 응답 속도(latency) 측정
- 평가 히스토리 DB 저장 및 조회
- 모델별 점수 비교 차트 시각화
- klue/roberta-base fine-tuning 품질 분류기 (Val Acc 0.9938)

## 🤖 Fine-tuning

- 모델: klue/roberta-base
- 데이터: 실제 수집 247개 + Synthetic 데이터 생성
- 학습: 5 epoch, Val Acc 0.9938
- 목적: LLM 응답 좋음/나쁨 이진 분류

## 🚀 실행 방법

### Backend
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Docker
```bash
docker build -t llm-eval-pipeline .
docker run -p 8000:8000 --env-file .env llm-eval-pipeline
```

## 📊 아키텍처
User → React Frontend → FastAPI Backend → Claude/GPT API

↓

SQLite DB (평가 히스토리)

↓

LLM-as-a-Judge 자동 평가

## 🔗 관련 프로젝트

- [pharma-risk-analyzer](https://github.com/leesihwan21/pharma-risk-analyzer) - RAG 기반 약물 부작용 분석 시스템