# display only the top {max_results} papers associated with the expert
def filter_papers(papers: list[dict], paper_ids: list[str], max_results: int = 5):
    # top papers associated with the author should be the one(s) that initially came up in the search
    priority_papers = [p for p in papers if p["paperId"] in paper_ids]

    # after that, show their most popular papers
    remaining_papers = [p for p in papers if p["paperId"] not in paper_ids]
    remaining_papers.sort(key=lambda p: p.get("citationCount", 0), reverse=True)

    combined = priority_papers + remaining_papers

    return combined[:max_results]

def get_expertise(papers: dict):
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