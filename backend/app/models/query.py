from pydantic import BaseModel
from typing import List

class Source(BaseModel):
    title: str
    url: str
    type: str

class Expert(BaseModel):
    name: str
    affiliation: str
    expertise: List[str]

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str
    sources: List[Source]
    experts: List[Expert]
