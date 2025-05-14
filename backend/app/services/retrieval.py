# from app.services.openai_chat import query_openai

# def get_expert_answer(question: str):
#     answer = query_openai(question)
#     return answer

from app.services.semantic_scholar import search_papers

def get_expert_answer(question: str):
    papers = search_papers(question)

    sources = []
    experts = []

    for paper in papers:
        sources.append({
            "title": paper["title"],
            "url": paper["url"],
            "type": paper.get("venue", "academic paper")
        })

        for author in paper.get("authors", []):
            expert = {
                "name": author["name"],
                "affiliation": "Unknown", # you can fetch more detail later with author id
                "expertise": [question] #placeholder for now
            }
            if expert not in experts:
                experts.append(expert)
        
    return {
        "answer": "Here are relevant sources and experts based on your question.",
        "sources": sources,
        "experts": experts
    }
