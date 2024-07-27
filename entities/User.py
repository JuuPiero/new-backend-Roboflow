from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from DB import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    projects = relationship("Project", back_populates="user")
    
    
    @staticmethod
    def Create(db: Session, user):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def GetById(db: Session, user_id: int):
        try:
            return db.query(User).filter(User.id == user_id).first()
        except:
            return False
    
    @staticmethod
    def GetByEmail(db: Session, email):
        try:
            return db.query(User).filter(User.email == email).first()
        except:
            return False
    
    @staticmethod
    def All(db: Session, skip: int = 0, limit: int = 10):
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def Update(db: Session, user_id: int, props: dict):
        user = User.GetById(db, user_id)
        if user:
            for key, value in props.items():
                if hasattr(user, key):
                    setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def DeleteById(db: Session, user_id: int):
        user = User.GetById(db, user_id)
        if user:
            db.delete(user)
            db.commit()
        return user