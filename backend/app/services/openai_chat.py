import json
from openai import OpenAI
import os

DEFAULT_SYSTEM_PROMPT = """You are an expert knowledge assistant. For the following question, provide:
  1. Multiple accredited and relevant experts in the field (if the topic has room for differing opinions, it is preferred that the choice of experts reflects that).
  1. A concise answer that these experts might respond with based on the literature you find online.
  2. Relevant sources (academic papers, articles, etc.) written by said experts, with proper URLs.

  Format the response as **JSON only** with this structure:
  {
    "experts": [{"name": "string", "affiliation": "string", "expertise": ["string"]}],
    "answer": "string",
    "sources": [{"title": "string", "url": "string", "type": "string"}],
  }
  Do not include any explanation outside the JSON.
  """

def query_openai(prompt: str) -> str:
  client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY"),
  )

  try:
    response = client.chat.completions.create(
      model = "gpt-3.5-turbo",
      messages = [
        # idea: add {domain} field and specifically tell the system to find experts that would
        # help to build an argument for {domain}
        {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
      ],
      # temperature = 0.7,
      # max_tokens = 300
    )

    content = response.choices[0].message.content.strip()

    try:
      return json.loads(content)
    except json.JSONDecodeError:
      print("Failed to parse JSON response:\n", content)
      return {
        "answer": "Error: Unable to parse AI response.",
        "sources": [],
        "experts": []
      }
  except RateLimitError as e:
    raise HTTPException(status_code=429, detail="You've exceeded your OpenAI quota. Please try again later.")