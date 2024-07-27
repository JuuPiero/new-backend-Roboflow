from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

from DB import Base

class Version(Base):
    __tablename__ = "versions"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'))
    
    project = relationship("Project", back_populates="versions")

    @staticmethod
    def Create(db: Session, version):
        db.add(version)
        db.commit()
        db.refresh(version)
        return version