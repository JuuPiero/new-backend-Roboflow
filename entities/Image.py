from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

from DB import Base

class Image(Base):
    __tablename__ = "images"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'))
    type = Column(String, index=True)
    image_name = Column(String, index=True)
    image_path = Column(String, index=True)
    label_path = Column(String, index=True, nullable=True)
    version_ids = Column(String, index=True, nullable=True)
    
    project = relationship("Project", back_populates="images")

    @staticmethod
    def Create(db: Session, image):
      
        db.add(image)
        db.commit()
        db.refresh(image)
        return image
    
    @staticmethod
    def GetByName(db: Session, image_name: int):
        try:
            return db.query(Image).filter(Image.image_name == image_name).first()
        except:
            return False