from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from db.connection import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    page_count = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())