from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from src.database.init import Base


class KataFile(Base):
    __tablename__ = 'kata_files'

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(String(255), unique=True)
    state = Column(String(255))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(),
                        onupdate=datetime.now())
