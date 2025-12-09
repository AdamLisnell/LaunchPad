from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from frameworks.fastapi.schemas.job import JobRead


class MatchRequest(BaseModel):
    candidate_id: str


class MatchResult(BaseModel):
    job: JobRead
    score: float
    match_reasons: List[str]


class MatchResponse(BaseModel):
    matches: List[MatchResult]