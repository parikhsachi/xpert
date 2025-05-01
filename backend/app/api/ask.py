from fastapi import APIRouter
from app.models.query import AskRequest, AskResponse
from app.services.retrieval import get_expert_answer

router = APIRouter()

@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    return get_expert_answer(request.question)