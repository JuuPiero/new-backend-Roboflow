from sqlalchemy import Column, Integer, String, Boolean ,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from DB import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    project_name = Column(String, index=True)
    project_type = Column(String, index=True)
    # visibility = Column(Boolean, index=True, default=False)
    classes = Column(String, index=True)

    user = relationship("User", back_populates="projects")
    images = relationship("Image", back_populates="project")
    versions = relationship("Version", back_populates="project")
    
    @staticmethod
    def Create(db: Session, project):
        db.add(project)
        db.commit()
        db.refresh(project)
        return project
    
    @staticmethod
    def GetById(db: Session, project_id: int):
        try:
            return db.query(Project).filter(Project.id == project_id).first()
        except:
            return False
    
    
    
    @staticmethod
    def Update(db: Session, project_id: int, props: dict):
        project = Project.GetById(db, project_id)
        if project:
            for key, value in props.items():
                if hasattr(project, key):
                    setattr(project, key, value)
        db.commit()
        db.refresh(project)
        return project
    
    
    @staticmethod
    def DeleteById(db: Session, project_id: int):
        project = Project.GetById(db, project_id)
        if project:
            db.delete(project)
            db.commit()
        return project
