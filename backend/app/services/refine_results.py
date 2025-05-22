from app.services.helpers.score_papers import combined_paper_score
from app.services.helpers.score_authors import combined_author_score

def rank_papers(papers: list[dict], length: int = 20) -> list[dict]:
    total = len(papers)
    scored_papers = []

    for i, paper in enumerate(papers):
        # use 2004 as default year? why not
        try:
            year = int(paper.get("year", 2004))
        except (TypeError, ValueError):
            year = 2004
        citations = paper.get("citationCount", 0)

        score = combined_paper_score(
            index = i,
            total = total,
            citations = citations,
            year = year
        )

        paper["score"] = score
        scored_papers.append(paper)

    # sort by descending score
    scored_papers.sort(key=lambda p: p["score"], reverse=True)

    for p in scored_papers:
        print(f"{p["title"]}\t{p["score"]}")
    return scored_papers[:length]

def rank_authors(authors: list[dict], length: int = 15) -> list[dict]:
    scored_authors = []

    for author in authors:
        score = combined_author_score(author)

        author["score"] = score
        scored_authors.append(author)

    scored_authors.sort(key=lambda a: a["score"], reverse=True)

    for a in scored_authors:
        print(f"{a["name"]}\t{a["score"]}")
    return scored_authors[:length]

# display only the top {max_results} papers associated with the expert
def filter_papers(papers: list[dict], paper_ids: list[str], max_results: int = 5) -> list[dict]:
    # top papers associated with the author should be the one(s) that initially came up in the search
    priority_papers = [p for p in papers if p["paperId"] in paper_ids]

    # after that, show their most popular papers
    remaining_papers = [p for p in papers if p["paperId"] not in paper_ids]
    remaining_papers.sort(key=lambda p: p.get("citationCount", 0), reverse=True)

    combined = priority_papers + remaining_papers

    return combined[:max_results]

def get_expertise(papers: dict) -> list:
    unique_fields = {}
    for paper in papers:
        fields = paper["fieldsOfStudy"] or []
        for field in fields:
            if field in unique_fields:
                unique_fields[field] += 1
            else:
                unique_fields[field] = 1
    
    sorted_fields = dict(sorted(unique_fields.items(), key=lambda item: item[1]))

    if len(sorted_fields) == 0:
        return ["No explicit fields of expertise found."]
    
    count = 0
    final_result = []
    for field in sorted_fields:
        final_result.append(field)
        count += 1
        if count == 5:
            break
    return final_result