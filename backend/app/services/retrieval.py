from app.services.semantic_scholar import search_papers
from app.services.semantic_scholar import search_authors
from app.services.refine_results import filter_papers
from app.services.refine_results import get_expertise
from app.services.orcid import get_orcid_profile
from app.services.orcid import get_orcid_affiliations
from app.services.openai_chat import query_openai
import time

min_h_index = 0

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

        # # import sample answers from json
        # from pathlib import Path
        # import json
        # sample_answers = None
        # TEMP_DIR = Path(__file__).resolve().parent.parent / "temp"
        # file_path = TEMP_DIR / "sample_answers.json"
        # with open(file_path, "r") as f:
        #     sample_answers = json.load(f)["answers"]
        # count = 0

        for author in authors:
            if author["hIndex"] < min_h_index:
                continue

            expertise = get_expertise(author["papers"])
            top_papers = filter_papers(author["papers"], paper_ids)

            affiliations = author["affiliations"]
            contact = {}

            # if affiliations missing, try ORCID
            if not affiliations or all(not a for a in affiliations):
                name_parts = author["name"].split()
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

            # # call GPT to get expert perspective
            # try:
            #     gpt_answer = query_openai(
            #         papers=author["papers"][:16],
            #         query=question,
            #         name=author["name"]
            #     )
            #     print(f"\nGPT response type: {type(gpt_answer)}\nContent: {gpt_answer}\n")
            #     time.sleep(1.5)  # avoid OpenAI rate limits
            # except Exception as e:
            #     print(f"OpenAI API call failed for {author['name']}: {e}")
            #     gpt_answer = "We couldn't generate an AI response for this expert at this time."
            gpt_answer = "Placeholder (not testing GPT right now)"

            expert = {
                "name": author["name"],
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
