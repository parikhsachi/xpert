from app.services.semantic_scholar import search_papers, search_authors
from app.services.refine_results import rank_papers, rank_authors, filter_papers, get_expertise
from app.services.orcid import get_orcid_profile, get_orcid_affiliations
from app.services.openai_chat import query_openai_bulk
from app.services.helpers.score_papers import relevance_score
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

    key_paper_ids = []
    author_score_boosts = {}

    for i, paper in enumerate(ranked_papers):
        paper_id = paper["paperId"]

        paper_rank_score = relevance_score(i, len(ranked_papers))

        # store paper ids, since these are likely the most relevant papers, so the model
        # shows each as the first paper associated with the affiliated expert
        if paper_id not in key_paper_ids:
            key_paper_ids.append(paper_id)
        paper_authors = paper.get("authors", [])
        for j, author in enumerate(paper_authors):
            author_id = author["authorId"]
            
            """
            For heuristic sorting before fetching list of author names, since Semantic Scholar likely
            won't be able to fetch all of the authors in one batch call.

            Authors get a +0.03 boost for being the first or last author listed, as they tend to be
            the lead contributor and the senior supervisor or principal investigator, respectively.
            https://blog.wordvice.com/journal-article-author-order/

            Authors get a +(0.07 * paper relevancy rank) boost, ensuring that the heuristic still
            prioritizes the findings of rank_papers
            """

            if j == 0 or j == len(paper_authors) - 1:
                author_score_boosts[author_id] = 0.03
            else:
                author_score_boosts[author_id] = 0
            
            author_score_boosts[author_id] += 0.07 * paper_rank_score

            print(f"Boost for {author["name"]}: {author_score_boosts[author_id]}\n")

    # Heuristically sort authors before querying Semantic Scholar
    sorted_authors_with_boosts = sorted(author_score_boosts.items(), key=lambda item: item[1], reverse=True)

    if ranked_papers:
        # rate limit of 1 request per second
        time.sleep(2)

        authors = search_authors(sorted_authors_with_boosts)
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
            top_papers = filter_papers(author["papers"], key_paper_ids)

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
