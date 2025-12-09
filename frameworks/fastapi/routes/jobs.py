from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException

from core.domain.job import Job
from core.use_cases.job_management import JobManagement    
from frameworks.fastapi.dependencies import get_job_management 
from frameworks.fastapi.schemas.job import JobCreate, JobRead, JobUpdate

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[JobRead])
async def list_jobs(
    skip: int = 0,
    limit: int = 100,
    job_management: JobManagement = Depends(get_job_management),
):
    """List jobs."""
    return await job_management.list_jobs(skip, limit)


@router.post("", response_model=JobRead, status_code=201)
async def create_job(
    job_data: JobCreate,
    job_management: JobManagement = Depends(get_job_management),
):
    """Create a new Job."""
    job = Job(**job_data.dict())
    return await job_management.create_job(job)


@router.get("/{job_id}", response_model=JobRead)
async def get_job(
    job_id: str, 
    job_management: JobManagement = Depends(get_job_management)
):
    """Get a Job by id."""
    job = await job_management.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.put("/{job_id}", response_model=JobRead)
async def update_job(
    job_id: str,
    job_data: JobUpdate,
    job_management: JobManagement = Depends(get_job_management),
):
    """Update a Job."""
    # Get existing Job
    existing_job = await job_management.get_job(job_id)
    if existing_job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    # Update fields
    for key, value in job_data.dict(exclude_unset=True).items():
        setattr(existing_job, key, value)

    # Save updated Job
    updated_job = await job_management.update_job(job_id, existing_job)
    return updated_job


@router.patch("/{job_id}")
async def patch_job(
    job_id: str,
    update_data: dict,
    job_management: JobManagement = Depends(get_job_management)
):
    """Partially update a job (for embeddings)."""
    try:
        # Get existing job
        existing_job = await job_management.get_job(job_id)
        if existing_job is None:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Update only provided fields
        if 'embedding' in update_data:
            existing_job.embedding = update_data['embedding']
        
        # Save updated job
        updated_job = await job_management.update_job(job_id, existing_job)
        
        return {
                "id": updated_job.id if updated_job else None,
                "title": updated_job.title if updated_job else "",
                "embedding_updated": 'embedding' in update_data
            }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{job_id}", response_model=bool)
async def delete_job(
    job_id: str, 
    job_management: JobManagement = Depends(get_job_management)
):
    """Delete a Job."""
    success = await job_management.delete_job(job_id)
    if not success:
        raise HTTPException(status_code=404, detail="Job not found")
    return success


@router.get("/category/{category}", response_model=List[JobRead])
async def get_jobs_by_category(
    category: str, 
    job_management: JobManagement = Depends(get_job_management)
):
    """Get jobs by category."""
    return await job_management.get_jobs_by_category(category)


@router.get("/available", response_model=List[JobRead])
async def get_available_jobs(
    job_management: JobManagement = Depends(get_job_management),
):
    """Get available jobs."""
    return await job_management.get_available_jobs()