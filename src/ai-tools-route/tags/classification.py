from enum import Enum
from pydantic import BaseModel, Field

class SentimentEnum(str, Enum):
    happy = "happy"
    sad = "sad"
    ok = "ok"

class AggressivenessEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Classification(BaseModel):
    sentiment: SentimentEnum = Field(..., description="Sentiment of the text")
    aggressiveness: AggressivenessEnum = Field(..., description="Aggressiveness of the text")
    language: str = Field(..., description="Language of the text")