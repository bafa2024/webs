from fastapi import APIRouter, Depends, HTTPException, status
from uuid import uuid4, UUID
from datetime import datetime
from typing import List
from .schemas import JobCreate, JobOut
from .auth import get_current_user

router = APIRouter()

# In-memory job store for demo
fake_jobs_db = {}

@router.post("/", response_model=JobOut)
def create_job(job: JobCreate, current_user: dict = Depends(get_current_user)):
    job_id = uuid4()
    now = datetime.utcnow()
    job_dict = {
        "id": job_id,
        "name": job.name,
        "settings": job.settings,
        "output_directory": job.output_directory,
        "status": "pending",
        "created_at": now,
        "updated_at": now,
        "total_pages": len(job.pages),
        "completed_pages": 0,
        "failed_pages": 0,
        "user_id": current_user["id"],
    }
    fake_jobs_db[str(job_id)] = job_dict
    return JobOut(**job_dict)

@router.get("/", response_model=List[JobOut])
def list_jobs(current_user: dict = Depends(get_current_user)):
    jobs = [JobOut(**job) for job in fake_jobs_db.values() if job["user_id"] == current_user["id"]]
    return jobs

@router.get("/{job_id}", response_model=JobOut)
def get_job(job_id: UUID, current_user: dict = Depends(get_current_user)):
    job = fake_jobs_db.get(str(job_id))
    if not job or job["user_id"] != current_user["id"]:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobOut(**job)

@router.delete("/{job_id}", status_code=204)
def delete_job(job_id: UUID, current_user: dict = Depends(get_current_user)):
    job = fake_jobs_db.get(str(job_id))
    if not job or job["user_id"] != current_user["id"]:
        raise HTTPException(status_code=404, detail="Job not found")
    del fake_jobs_db[str(job_id)]
    return 