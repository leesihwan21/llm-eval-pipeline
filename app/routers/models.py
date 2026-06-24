from fastapi import APIRouter

router = APIRouter()

@router.get("/list")
async def get_models():
    return {
        "models": [
            {"id": "gpt-4o", "provider": "openai"},
            {"id": "claude-sonnet-4-6", "provider": "anthropic"},
            {"id": "llama-3", "provider": "meta"},
        ]
    }