import os
import requests

API_URL = "https://api.semanticscholar.org/graph/v1"
API_KEY = os.getenv("S2_API_KEY")

HEADERS = {
    "x-api-key": API_KEY
}

def search_papers(query: str, limit=5):
    # for testing
    from pathlib import Path
    import json
    TEMP_DIR = Path(__file__).resolve().parent.parent / "temp"
    file_path = TEMP_DIR / "2025-05-14T11-59-54.434454.json"
    with open(file_path, "r") as f:
        return json.load(f)["data"]

    # ===== Remove above lines when we're ready for real testing =====

    url = f"{API_URL}/paper/search"
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,authors,url,venue,year,fieldsOfStudy"
    }
    response = requests.get(url, headers=HEADERS, params=params)

    # check for error
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("[SemanticScholar] HTTPError:", e)
        print("[SemanticScholar] Response:", response.text)
        return {}

    json_data = response.json()
    # check for malformatted response
    if "data" not in json_data:
        print("[SemanticScholar] Unexpected response:", json_data)
        return {}

    # # dump file to temp file for testing
    # from pathlib import Path

    # # Resolve the absolute path to the 'temp' directory
    # TEMP_DIR = Path(__file__).resolve().parent.parent / "temp"
    # TEMP_DIR.mkdir(parents=True, exist_ok=True)  # Create it if it doesn't exist

    # # Example: create timestamped filename
    # from datetime import datetime
    # import json

    # timestamp = datetime.now().isoformat().replace(":", "-")  # Safe for filenames
    # file_path = TEMP_DIR / f"{timestamp}.json"

    # # Example usage: write JSON data to the file
    # with open(file_path, "w") as f:
    #     json.dump(response.json(), f, indent=2)
    
    return response.json()["data"]