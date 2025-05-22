import requests

def get_orcid_profile(author: dict):
    """Tries to get ORCID data using Semantic Scholar's result first, then falls back to name search."""
    orcid_id = author.get("orcid")

    if not orcid_id:
        # if there is no ORCID ID found on the author's semantic scholar page, fallback to name-based search
        given_name = author.get("givenName") or author.get("name", "").split()[0]
        family_name = author.get("familyName") or author.get("name", "").split()[-1]

        print("[ORCID] ORCID ID not found in Semantic Scholar, searching by name:", given_name, family_name)
        orcid_id = get_orcid_id_by_name(given_name, family_name)
    
    # use provided ORCID ID directly
    print("[ORCID] Found ORCID in Semantic Scholar:", orcid_id)
    profile_data = get_orcid_profile_by_id(orcid_id)

    return profile_data, orcid_id


def get_orcid_profile_by_id(orcid_id: str):
    """Fetch ORCID profile using known ORCID ID."""
    if not orcid_id:
        return None
    
    url = f"https://pub.orcid.org/v3.0/{orcid_id}/person"
    headers = {"Accept": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        profile_data = response.json()

        # import pprint
        # pprint.pp(profile_data)

        # if orcid_id == "0000-0001-6693-0786":
        #     # dump file to temp file for testing
        #     from pathlib import Path

        #     # Resolve the absolute path to the 'temp' directory
        #     TEMP_DIR = Path(__file__).resolve().parent.parent / "temp"
        #     TEMP_DIR.mkdir(parents=True, exist_ok=True)  # Create it if it doesn't exist

        #     # Example: create timestamped filename
        #     from datetime import datetime
        #     import json

        #     timestamp = datetime.now().isoformat().replace(":", "-")  # Safe for filenames
        #     file_path = TEMP_DIR / f"orcid-cinzia-calluso-{timestamp}.json"

        #     # Example usage: write JSON data to the file
        #     with open(file_path, "w") as f:
        #         json.dump(profile_data, f, indent=2)

        return profile_data
    except Exception as e:
        print("[ORCID] Exception fetching by ID:", e)
        return None

def get_orcid_id_by_name(given_name: str, family_name: str) -> str:
    """Fallback: Search ORCID by name if ID is not known."""
    query = f'{given_name} {family_name}'
    url = "https://pub.orcid.org/v3.0/search/"
    headers = {"Accept": "application/json"}
    params = {"q": f'given-names:"{given_name}" AND family-name:"{family_name}"'}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if not isinstance(data, dict):
            print("[ORCID] Unexpected response type:", type(data))
            return None

        if "result" not in data or not data["result"]:
            print("[ORCID] No results for:", given_name, family_name)
            return None

        orcid_id = data["result"][0]["orcid-identifier"]["path"]
        
        return orcid_id
    except Exception as e:
        print("[ORCID] Exception:", e)
        return None

def get_orcid_affiliations(orcid_id: str) -> list:
    url = f"https://pub.orcid.org/v3.0/{orcid_id}/employments"
    headers = {"Accept": "application/json"}
    resp = requests.get(url, headers=headers)

    if resp.status_code != 200:
        print(f"[ORCID] Error fetching employments for {orcid_id}")
        return []

    data = resp.json()
    summaries = data.get("employment-summary", [])
    return [s["organization"]["name"] for s in summaries if "organization" in s]
