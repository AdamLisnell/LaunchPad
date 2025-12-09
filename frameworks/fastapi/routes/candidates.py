from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException

from core.domain.candidate import Candidate
from core.use_cases.candidate_management import CandidateManagement
from frameworks.fastapi.dependencies import get_candidate_management
from frameworks.fastapi.schemas.candidate import CandidateCreate, CandidateRead, CandidateUpdate

router = APIRouter(
    prefix="/candidates",
    tags=["candidates"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[CandidateRead])
async def list_candidates(
    skip: int = 0,
    limit: int = 100,
    candidate_management: CandidateManagement = Depends(get_candidate_management),
):
    """List candidates."""
    return await candidate_management.list_candidates(skip, limit)


@router.post("", response_model=CandidateRead, status_code=201)
async def create_candidate(
    candidate_data: CandidateCreate,
    candidate_management: CandidateManagement = Depends(get_candidate_management),
):
    """Create a new Candidate."""
    candidate = Candidate(**candidate_data.dict())
    return await candidate_management.create_candidate(candidate)


@router.get("/{candidate_id}", response_model=CandidateRead)
async def get_candidate(
    candidate_id: str,
    candidate_management: CandidateManagement = Depends(get_candidate_management),
):
    """Get a Candidate by id."""
    candidate = await candidate_management.get_candidate(candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate


@router.put("/{candidate_id}", response_model=CandidateRead)
async def update_candidate(
    candidate_id: str,
    candidate_data: CandidateUpdate,
    candidate_management: CandidateManagement = Depends(get_candidate_management),
):
    """Update a Candidate."""
    # Get existing Candidate
    existing_candidate = await candidate_management.get_candidate(candidate_id)
    if existing_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")

    # Update fields
    for key, value in candidate_data.dict(exclude_unset=True).items():
        setattr(existing_candidate, key, value)

    # Save updated Candidate
    updated_candidate = await candidate_management.update_candidate(
        candidate_id, existing_candidate
    )
    return updated_candidate


@router.delete("/{candidate_id}", response_model=bool)
async def delete_candidate(
    candidate_id: str,
    candidate_management: CandidateManagement = Depends(get_candidate_management),
):
    """Delete a Candidate."""
    success = await candidate_management.delete_candidate(candidate_id)
    if not success:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return success