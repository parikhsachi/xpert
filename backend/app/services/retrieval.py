# from app.services.openai_chat import query_openai

# def get_expert_answer(question: str):
#     answer = query_openai(question)
#     return answer

from app.services.semantic_scholar import search_papers
from app.services.semantic_scholar import search_authors
from app.services.refine_results import filter_papers
from app.services.refine_results import get_expertise
import time

def get_expert_answer(question: str):
    papers = search_papers(question)

    paper_ids = []
    author_ids = []

    for paper in papers:
        paper_id = paper["paperId"]
        # store paper ids, since these are likely the most relevant papers, so the model
        # shows each as the first paper associated with the affiliated expert
        if paper_id not in paper_ids:
            paper_ids.append(paper_id)
        for author in paper.get("authors", []):
            author_id = author["authorId"]
            if author_id not in author_ids:
                author_ids.append(author_id) 

    if papers:
        # rate limit of 1 request per second
        time.sleep(2)

        authors = search_authors(author_ids)

        experts = []

        for author in authors:
            if author["hIndex"] < 1:
                continue

            expertise = get_expertise(author["papers"])

            top_papers = filter_papers(author["papers"], paper_ids)

            expert = {
                "name": author["name"],
                "url": author["url"],
                "affiliations": author["affiliations"] or ["No affiliations found"],
                "hIndex": author["hIndex"],
                "expertise": expertise,
                "paperCount": author["paperCount"],
                "papers": top_papers,
                "answer": "Placeholder for sample author opinion on the topic.",
            }
            if expert not in experts:
                experts.append(expert)

        return {
            "numExperts": len(experts),
            "experts": experts,
        }
    else:
        return {
            "numExperts": 0,
            "experts": [],
            "error": "Sorry, we were unable to retrieve any papers related to your query.",
        }
