from sqlalchemy.orm import Session
from models.user import User


class UserRepository:

    # def get_by_email(self, db: Session, email: str):
    #     return db.query(User).filter(User.email == email).first()
    def get_by_username(self, db: Session, username: str):
        return db.query(User).filter(User.username == username).first()
    
    def create(self, db: Session, user: User):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def activate_account(self, db: Session, username: str):
        user = self.get_by_username(db, username)
        if user:
            user.is_active = True
            db.commit()
            return user
        return None
    
    def update_password(self, db: Session, user: User, hashed_password: str):
        user.hashed_password = hashed_password
        db.commit()
        db.refresh(user)
        return user