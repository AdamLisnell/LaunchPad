from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException

from core.domain.requirement import Requirement
from core.use_cases.requirement_management import RequirementManagement
from frameworks.fastapi.dependencies import get_requirement_management
from frameworks.fastapi.schemas.requirement import (
    RequirementCreate,
    RequirementRead,
    RequirementUpdate,
)

router = APIRouter(
    prefix="/requirements",
    tags=["requirements"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[RequirementRead])
async def list_requirements(
    skip: int = 0,
    limit: int = 100,
    requirement_management: RequirementManagement = Depends(get_requirement_management),
):
    """List requirements."""
    return await requirement_management.list_requirements(skip, limit)


@router.post("", response_model=RequirementRead, status_code=201)
async def create_requirement(
    requirement_data: RequirementCreate,
    requirement_management: RequirementManagement = Depends(get_requirement_management),
):
    """Create a new Requirement."""
    # Create Requirement object
    requirement = Requirement(**requirement_data.dict())
    return await requirement_management.create_requirement(requirement)


@router.get("/{requirement_id}", response_model=RequirementRead)
async def get_requirement(
    requirement_id: str,
    requirement_management: RequirementManagement = Depends(get_requirement_management),
):
    """Get a Requirement by id."""
    requirement = await requirement_management.get_requirement(requirement_id)
    if requirement is None:
        raise HTTPException(status_code=404, detail="Requirement not found")
    return requirement


@router.put("/{requirement_id}", response_model=RequirementRead)
async def update_requirement(
    requirement_id: str,
    requirement_data: RequirementUpdate,
    requirement_management: RequirementManagement = Depends(get_requirement_management),
):
    """Update a Requirement."""
    # Get existing Requirement
    existing_requirement = await requirement_management.get_requirement(requirement_id)
    if existing_requirement is None:
        raise HTTPException(status_code=404, detail="Requirement not found")

    # Update fields
    for key, value in requirement_data.dict(exclude_unset=True).items():
        setattr(existing_requirement, key, value)

    # Save updated Requirement
    updated_requirement = await requirement_management.update_requirement(
        requirement_id, existing_requirement
    )
    return updated_requirement


@router.delete("/{requirement_id}", response_model=bool)
async def delete_requirement(
    requirement_id: str,
    requirement_management: RequirementManagement = Depends(get_requirement_management),
):
    """Delete a Requirement."""
    success = await requirement_management.delete_requirement(requirement_id)
    if not success:
        raise HTTPException(status_code=404, detail="Requirement not found")
    return success


@router.get("/ordered", response_model=List[RequirementRead])
async def get_ordered_requirements(
    requirement_management: RequirementManagement = Depends(get_requirement_management),
):
    """Get requirements ordered by their order field."""
    return await requirement_management.get_ordered_requirements()