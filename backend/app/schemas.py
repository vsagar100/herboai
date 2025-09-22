from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class QueryRequest(BaseModel):
    query: str  # Frontend sends "query" not "question"
    lang: Optional[str] = "en"

class HerbRemedySchema(BaseModel):
    condition: str
    preparation: str
    dosage: Optional[str] = None

class HerbDataSchema(BaseModel):
    id: str
    name: str
    scientific_name: Optional[str] = ""
    common_names: List[str] = []
    uses: str
    ayush_system: Optional[str] = "Ayurveda"
    parts_used: Optional[str] = ""
    contraindications: Optional[str] = ""
    dosage: Optional[str] = ""
    remedies: List[HerbRemedySchema] = []
    description: Optional[str] = ""

class QueryMetadata(BaseModel):
    language: str
    query_length: Optional[int] = 0
    herbs_found: Optional[int] = 0
    sources_used: Optional[int] = 0
    confidence: Optional[float] = 0.0
    intent: Optional[str] = "general_health"
    error: Optional[bool] = False

class QueryAnswer(BaseModel):
    success: bool
    ai_response: str
    results: List[HerbDataSchema] = []  # Frontend expects "results" not "sources"
    metadata: QueryMetadata

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    ai_response: str
    results: List[Any] = []
    metadata: Dict[str, Any] = {}