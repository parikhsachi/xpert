import math
from datetime import datetime

# Calculate relevance score from 0 to 1
def relevance_score(idx: int, total: int) -> float:
    return math.log(idx + 1) / math.log(total + 1)

# Calculate citation score from 0 to 1
def citation_score(citations: int, max_citations: int=5000) -> float:
    # Clamp to avoid log(0)
    citations = max(1, citations)
    return min(math.log(citations + 1) / math.log(max_citations + 1), 1.0)

# Calculate recency score from 0 to 1
def recency_score(year: int, decay_factor: float=0.5, half_life: int=7) -> float:
    current_year = datetime.now().year
    age = max(0, current_year - year)
    return decay_factor ** (age / half_life)

# Give paper a score
def combined_paper_score(index: int, total: int, citations: int, year: int, weights=(0.4, 0.3, 0.3)) -> float:
    relevance_weight, citation_weight, recency_weight = weights
    return (
        relevance_weight * relevance_score(index, total) +
        citation_weight * citation_score(citations) +
        recency_weight * recency_score(year)
    )