from pydantic import BaseModel
from typing import List, Optional

class Paper(BaseModel):
    title: str
    url: str
    year: Optional[int] = None
    citationCount: Optional[int] = 0
    fieldsOfStudy: Optional[List[str]] = None

class Expert(BaseModel):
    name: str
    url: str
    affiliations: List[str]
    hIndex: int
    expertise: List[str]
    paperCount: int
    papers: List[Paper]
    answer: str

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    # answer: str
    # sources: List[Source]
    numExperts: int
    experts: List[Expert]
    error: Optional[str] = None
