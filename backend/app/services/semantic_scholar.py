import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.semanticscholar.org/graph/v1"
API_KEY = os.getenv("S2_API_KEY")

HEADERS = {
    "x-api-key": API_KEY
}

def search_papers(query: str, limit=25):
    # # for testing
    # from pathlib import Path
    # import json
    # TEMP_DIR = Path(__file__).resolve().parent.parent / "temp"
    # file_path = TEMP_DIR / "papers-illegal-immigration.json"
    # with open(file_path, "r") as f:
    #     return json.load(f)["data"]

    # ===== Remove above lines when we're ready for real testing =====

    url = f"{API_URL}/paper/search"
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,authors,url,venue,year,fieldsOfStudy,citationCount"
    }
    response = requests.get(url, headers=HEADERS, params=params)

    # check for error
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("[SemanticScholar/paper] HTTPError:", e)
        print("[SemanticScholar/paper] Response:", response.text)
        return []

    json_data = response.json()
    # check for malformatted response
    if "data" not in json_data:
        print("[SemanticScholar/paper] Unexpected response:", json_data)
        return []

    # # dump file to temp file for testing
    # from pathlib import Path

    # # Resolve the absolute path to the 'temp' directory
    # TEMP_DIR = Path(__file__).resolve().parent.parent / "temp"
    # TEMP_DIR.mkdir(parents=True, exist_ok=True)  # Create it if it doesn't exist

    # # Example: create timestamped filename
    # from datetime import datetime
    # import json

    # timestamp = datetime.now().isoformat().replace(":", "-")  # Safe for filenames
    # file_path = TEMP_DIR / f"papers-{timestamp}.json"

    # # Example usage: write JSON data to the file
    # with open(file_path, "w") as f:
    #     json.dump(json_data, f, indent=2)
    
    return json_data["data"]

def search_authors(sorted_author_tuples: list[tuple[str, float]]):
    # # for testing
    # from pathlib import Path
    # import json
    # TEMP_DIR = Path(__file__).resolve().parent.parent / "temp"
    # file_path = TEMP_DIR / "authors-illegal-immigration.json"
    # with open(file_path, "r") as f:
    #     return json.load(f)

    # ===== Remove above lines when we're ready for real testing =====
    ids_plus_score_boosts = dict(sorted_author_tuples)

    ids = list(ids_plus_score_boosts.keys())

    url = f"{API_URL}/author/batch"
    params = {
        "fields": "name,url,affiliations,hIndex,paperCount,papers,papers.title,papers.url,papers.year,papers.citationCount,papers.fieldsOfStudy,papers.abstract"
    }
    json = {
        "ids": ids[:27]
    }

    response = requests.post(url, headers=HEADERS, params=params, json=json)

    # check for error
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("[SemanticScholar/author] HTTPError:", e)
        print("[SemanticScholar/author] Response:", response.text)
        return []

    json_data = response.json()
    # check for malformatted response
    if len(json_data) == 0 or "authorId" not in json_data[0]:
        print("[SemanticScholar/author] Unexpected response:", json_data)
        return []
    
    for author in json_data:
        author["score"] = ids_plus_score_boosts.get(author["authorId"], 0)
    
    # dump file to temp file for testing
    from pathlib import Path

    # Resolve the absolute path to the 'temp' directory
    TEMP_DIR = Path(__file__).resolve().parent.parent / "temp"
    TEMP_DIR.mkdir(parents=True, exist_ok=True)  # Create it if it doesn't exist

    # Example: create timestamped filename
    from datetime import datetime
    import json

    timestamp = datetime.now().isoformat().replace(":", "-")  # Safe for filenames
    file_path = TEMP_DIR / f"authors-{timestamp}.json"

    # Example usage: write JSON data to the file
    with open(file_path, "w") as f:
        json.dump(json_data, f, indent=2)
    
    return json_data
