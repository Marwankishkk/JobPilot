from sqlalchemy import Boolean, Column, Integer, String
from core.db import Base

    

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    company = Column(String, nullable=False)
    location = Column(String, nullable=True)
    status = Column(String, default="applied", nullable=False)
    applied_date = Column(String, nullable=True)
    user_id = Column(Integer,index=True ,nullable=False)