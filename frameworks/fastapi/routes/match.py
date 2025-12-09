from typing import List
from fastapi import APIRouter, Depends, HTTPException

from core.use_cases.match_jobs import MatchJobs 
from core.use_cases.candidate_management import CandidateManagement
from frameworks.fastapi.dependencies import get_match_jobs, get_candidate_management
from frameworks.fastapi.schemas.match import MatchRequest, MatchResponse, MatchResult
from frameworks.fastapi.schemas.job import JobRead

router = APIRouter(
    prefix="/match",
    tags=["match"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=MatchResponse)
async def match_jobs(
    match_request: MatchRequest,
    match_jobs_use_case: MatchJobs = Depends(get_match_jobs),
    candidate_management: CandidateManagement = Depends(get_candidate_management),
):
    """Match jobs for a candidate using semantic similarity."""
    # Get candidate
    candidate = await candidate_management.get_candidate(match_request.candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")

    # Match jobs
    match_results = await match_jobs_use_case.match_jobs_for_profile(candidate)

    # Convert domain entities to response schemas
    matches = []
    for result in match_results:
        matches.append(
            MatchResult(
                job=JobRead.from_orm(result["job"]),
                score=result["score"],
                match_reasons=result["match_reasons"],
            )
        )

    return MatchResponse(matches=matches)


@router.post("/fallback", response_model=MatchResponse)
async def fallback_match(
    match_request: MatchRequest,
    match_jobs_use_case: MatchJobs = Depends(get_match_jobs),
    candidate_management: CandidateManagement = Depends(get_candidate_management),
):
    """Fallback match jobs for a candidate without embeddings."""
    # Get candidate
    candidate = await candidate_management.get_candidate(match_request.candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")

    # Match jobs using fallback
    match_results = await match_jobs_use_case.fallback_match(candidate)

    # Convert domain entities to response schemas
    matches = []
    for result in match_results:
        matches.append(
            MatchResult(
                job=JobRead.from_orm(result["job"]),
                score=result["score"],
                match_reasons=result["match_reasons"],
            )
        )

    return MatchResponse(matches=matches)