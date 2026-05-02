from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session

from schemas.job import (
   JobCreate,
   JobUpdate
)
from services.job_service import JobService
from services.user_service import UserService
from core.db import get_db

router = APIRouter(prefix="/jobs", tags=["Jobs"])

service = JobService()
user_service = UserService()

@router.post("/")
def create_job(
    job_data: JobCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        email = user_service.get_current_user(token)
        user = user_service.repo.get_by_email(db, email)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    try:
        return service.create_job(db, job_data, user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/")
def get_jobs(
    request: Request,
    db: Session = Depends(get_db)
):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        email = user_service.get_current_user(token)
        user = user_service.repo.get_by_email(db, email)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    return service.get_jobs_by_user(db, user.id)

@router.put("/{job_id}")
def update_job(
    job_id: int,
    job_data: JobUpdate,
    request: Request,
    db: Session = Depends(get_db)
):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        email = user_service.get_current_user(token)
        user = user_service.repo.get_by_email(db, email)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    try:
        return service.update_job(db, job_id, job_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        email = user_service.get_current_user(token)
        user = user_service.repo.get_by_email(db, email)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    try:
        service.delete_job(db, job_id)
        return Response(status_code=204)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))