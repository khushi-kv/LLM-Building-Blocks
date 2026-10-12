from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: str

class QueryAnalysis(BaseModel):
    intent: str
    sentiment: str
    topics: list[str]
    confidence_score: float