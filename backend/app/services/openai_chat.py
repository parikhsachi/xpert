import json
from openai import OpenAI
import os

BASE_SYSTEM_PROMPT = """You are an expert knowledge interpreter. Based on the article abstracts provided by co-author provided, \
generate a sample expert perspective (1 paragraph or less) on the topic provided by the user. The summary should be concise, \
insightful, and helpful to a user trying to learn about the topic. It should be written in an assertive voice, and ensure that \
the perspective/argument is clearly displayed at the front such that it is clearly conveyed to the user. Do not include the \
abstracts or titles in the response.
Return ONLY a valid JSON list of objects. Each object should have:
  - "authorId": string (copied from input)
  - "perspective": string (1 paragraph, assertive and concise)
No intro, no explanations. Strict JSON only.
"""

BASE_PROMPT = """The user has asked: '{query}'\n\nHere are multiple experts and the abstracts of their papers. Write a \
clear, assertive perspective on the topic for each expert based on their work. Carefully ensure that you write a paragraph \
for EACH of the {count} authors\n\n
"""

def query_openai_bulk(authors: list[dict], query: str) -> dict:
  # return {}
  client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY"),
  )

  system_prompt = BASE_SYSTEM_PROMPT

  prompt = BASE_PROMPT.format(query=query, count=len(authors))

  for author in authors:
    author_id = author["authorId"]
    prompt += f"## Author ID: {author_id}\n"
    name = author["name"]
    prompt += f"## Name: {name}\n"
    for paper in author["papers"]:
      title = paper.get("title", "No title")
      abstract = paper.get("abstract", "No abstract")
      prompt += f"Title: {title}\nAbstract: {abstract}\n\n"
  
  print(prompt)

  try:
    response = client.chat.completions.create(
      model = "gpt-4-turbo",
      messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
      ],
      # temperature = 0.7,
      # max_tokens = 300
    )

    output_text = response.choices[0].message.content.strip()

    try:
      parsed = json.loads(output_text)
      return {entry["authorId"]: entry["perspective"] for entry in parsed}
    except Exception as e:
      print("[GPT parsing error]", e)
      print("[GPT raw output]", output_text)
      return {}

  except RateLimitError as e:
    raise HTTPException(status_code=429, detail="You've exceeded your OpenAI quota. Please try again later.")