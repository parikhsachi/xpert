from app.services.openai_chat import query_openai

def get_expert_answer(question: str):
    answer = query_openai(question)
    return answer
