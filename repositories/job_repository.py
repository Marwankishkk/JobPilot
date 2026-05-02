from sqlalchemy.orm import Session
from models.user import User
from models.job import Job
from schemas.job import  JobUpdate
class JobRepository:
    def get_by_id(self, db: Session, job_id: int):
        return db.query(Job).filter(Job.id == job_id).first()
    
    def create(self, db: Session, job_in, user_id):
        new_job = Job(
            title=job_in.title,
            description=job_in.description,
            company=job_in.company,
            location=job_in.location,
            status=job_in.status,
            applied_date=job_in.applied_date,
            user_id=user_id
        )
        db.add(new_job)
        db.commit()
        db.refresh(new_job)
        return new_job
      
    def get_by_user(self, db: Session, user_id):
            return db.query(Job).filter(Job.user_id == user_id).all()
    
    def update(self, db: Session, job:Job , job_in : JobUpdate):
        update_data = job_in.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(job, key, value)

        db.commit()
        db.refresh(job)
        return job

    def delete(self, db: Session, job_id: int):
        job = self.get_by_id(db, job_id)
        if job:
            db.delete(job)
            db.commit()
            return True
        return False
    