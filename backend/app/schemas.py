from typing import List, Optional, Literal
from pydantic import BaseModel, Field

Lang = Literal["en", "hi", "mr"]

class HerbRef(BaseModel):
    type: Literal["text","paper","url"]
    source: str
    url: Optional[str] = ""

class HerbLang(BaseModel):
    short_description: str
    long_description: str

class Herb(BaseModel):
    id: str = Field(..., examples=["herb_0001"])
    name: str
    scientific_name: Optional[str] = None
    ayush_system: List[str] = ["Ayurveda"]
    synonyms: List[str] = []
    parts_used: List[str] = []
    uses: str = ""
    phytochemicals: str = ""
    dosage: str = ""
    contraindications: str = ""
    formulations: List[str] = []
    references: List[HerbRef] = []
    languages: dict[Lang, HerbLang]
    examples: List[str] = []

class QueryRequest(BaseModel):
    question: str
    lang: Optional[Lang] = None  # if None → auto detect
    top_k: int = 4

class QueryAnswer(BaseModel):
    answer: str
    lang: Lang
    sources: List[str]  # herb ids

class SearchResponse(BaseModel):
    matches: List[dict]