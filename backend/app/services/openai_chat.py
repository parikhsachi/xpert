import json
from openai import OpenAI
import os

BASE_SYSTEM_PROMPT = """You are an expert knowledge interpreter. Based on the article abstracts provided by co-author provided, \
  generate a sample expert perspective (1 paragraph or less) on the topic provided by the user. The summary should be concise, \
  insightful, and helpful to a user trying to learn about the topic. It should be written in an assertive voice, and ensure that \
  the perspective/argument is clearly displayed at the front such that it is clearly conveyed to the user. Do not include the \
  abstracts or titles in the response.
  """

BASE_PROMPT = """##Name: {name}
  ###Topic: '{query}'
  ###Papers:\n"
"""

def query_openai(papers: str, query: str, name: str) -> str:
  if papers == []:
    return f"Error: not enough info found about {name} to generate perspective"

  client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY"),
  )

  system_prompt = BASE_SYSTEM_PROMPT.format(name=name, query=query)

  prompt = BASE_PROMPT.format(name=name, query=query)

  for paper in papers:
    title = paper["title"]
    abstract = "No abstract found"
    if "abstract" in paper:
      abstract = paper["abstract"]
    prompt += f"Title: {title}\nAbstract: {abstract}\n\n"

  try:
    response = client.chat.completions.create(
      model = "gpt-3.5-turbo",
      messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
      ],
      # temperature = 0.7,
      # max_tokens = 300
    )

    return response.choices[0].message.content.strip()

  except RateLimitError as e:
    raise HTTPException(status_code=429, detail="You've exceeded your OpenAI quota. Please try again later.")