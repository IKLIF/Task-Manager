import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True),  primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String)#, unique=True)#, index=True)
    description = Column(String)
    status = Column(String)