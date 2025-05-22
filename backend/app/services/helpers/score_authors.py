from datetime import datetime
from app.services.helpers.score_papers import combined_paper_score

def combined_author_score(author: dict) -> float:
    h_index = author.get("hIndex", 0)
    paper_count = author.get("paperCount", 0)
    papers = author.get("papers", [])

    # Fallback if no papers exist
    if not papers:
        return 0.0

    current_year = datetime.now().year
    top_paper_score = 0
    most_recent_year = 2004

    for idx, paper in enumerate(papers):
        citations = paper.get("citationCount", 0)
        year = int(paper.get("year", 2004) or 2004)
        score = combined_paper_score(idx, len(papers), citations, year)
        top_paper_score = max(top_paper_score, score)
        most_recent_year = max(most_recent_year, year)

    recency_score = 1.0 - ((current_year - most_recent_year) / 20.0)
    recency_score = max(0.0, min(recency_score, 1.0))

    return (
        0.4 * min(h_index / 100.0, 1.0) +           # Normalize h-index to 0–1
        0.1 * min(paper_count / 100.0, 1.0) +       # Normalize paper count to 0–1
        0.3 * top_paper_score +                     # Already normalized 0–1
        0.2 * recency_score                         # Decay for freshness
    )