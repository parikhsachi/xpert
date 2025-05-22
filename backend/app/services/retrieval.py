from app.services.semantic_scholar import search_papers, search_authors
from app.services.refine_results import rank_papers, rank_authors, filter_papers, get_expertise
from app.services.orcid import get_orcid_profile, get_orcid_affiliations
from app.services.openai_chat import query_openai_bulk
import time

min_h_index = 0

def get_expert_answer(question: str):
    papers = search_papers(question)
    if not papers:
        return {
            "numExperts": 0,
            "experts": [],
            "error": "No papers were returned for this query. Please try a different question."
        }

    ranked_papers = rank_papers(papers)

    paper_ids = []
    author_ids = []

    for paper in ranked_papers:
        paper_id = paper["paperId"]
        # store paper ids, since these are likely the most relevant papers, so the model
        # shows each as the first paper associated with the affiliated expert
        if paper_id not in paper_ids:
            paper_ids.append(paper_id)
        for author in paper.get("authors", []):
            author_id = author["authorId"]
            if author_id not in author_ids:
                author_ids.append(author_id) 

    if ranked_papers:
        # rate limit of 1 request per second
        time.sleep(2)

        authors = search_authors(author_ids)
        ranked_authors = rank_authors(authors)

        experts = []

        # # import sample answers from json
        # from pathlib import Path
        # import json
        # sample_answers = None
        # TEMP_DIR = Path(__file__).resolve().parent.parent / "temp"
        # file_path = TEMP_DIR / "sample_answers.json"
        # with open(file_path, "r") as f:
        #     sample_answers = json.load(f)["answers"]
        # count = 0

        # call GPT to get expert perspective
        try:
            author_data = [
                {"name": author["name"], "authorId": author["authorId"], "papers": author["papers"][:5]}
                for author in ranked_authors
                if author["hIndex"] >= min_h_index
            ]
            gpt_answers = query_openai_bulk(authors=author_data, query=question)
            print(f"\nGPT response type: {type(gpt_answers)}\nContent: {gpt_answers}\n")
        except Exception as e:
            print(f"OpenAI API call failed: {e}")
            gpt_answers = {}

        for author in ranked_authors:
            if author["hIndex"] < min_h_index:
                continue

            name = author["name"]
            expertise = get_expertise(author["papers"])
            top_papers = filter_papers(author["papers"], paper_ids)

            affiliations = author["affiliations"]
            contact = {}

            gpt_answer = gpt_answers.get(author["authorId"], "We couldn't generate a response for this expert.")

            # if affiliations missing, try ORCID
            if not affiliations or all(not a for a in affiliations):
                name_parts = name.split()
                result = get_orcid_profile(author)
                if result:
                    orcid_data, orcid_id = result
                    if orcid_data:
                        affiliations = get_orcid_affiliations(orcid_id)

                        # Try to get contact info

                        # Emails
                        emails = orcid_data.get("emails", {}).get("email", [])
                        contact["emails"] = [e["email"] for e in emails if e.get("email")]

                        # Researcher URLs
                        urls = orcid_data.get("researcher-urls", {}).get("researcher-url", [])
                        for u in urls:
                            print(u["url"]["value"])
                        contact["researcher-urls"] = [
                            {
                                "name": u["url-name"],
                                "url": u["url"]["value"]
                            }
                            for u in urls
                            if u.get("url", {}).get("value")
                        ]

                        # External Identifiers
                        ext_ids = orcid_data.get("external-identifiers", {}).get("external-identifier", [])
                        contact["external-identifiers"] = [
                            {
                                "name": i["source"]["source-name"]["value"],
                                "url": i["external-id-url"]["value"]
                            }
                            for i in ext_ids
                            if i.get("external-id-url", {}).get("value")
                        ]

            expert = {
                "name": name,
                "url": author["url"],
                "affiliations": affiliations or ["No affiliations found"],
                "hIndex": author["hIndex"],
                "expertise": expertise,
                "paperCount": author["paperCount"],
                "papers": top_papers,
                "answer": gpt_answer,
                "contact": contact
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
