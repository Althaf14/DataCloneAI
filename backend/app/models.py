from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    REVIEWER = "reviewer"

class DocStatus(str, enum.Enum):
    PROCESSING = "processing"
    FLAGGED = "flagged"
    VERIFIED = "verified"

class DocType(str, enum.Enum):
    ID_PROOF = "ID_PROOF"
    CERTIFICATE = "CERTIFICATE"

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            value = value.upper() # Match against uppercase names/values
            for member in cls:
                if member.value == value:
                    return member
        return None

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(255))
    role = Column(Enum(UserRole), default=UserRole.REVIEWER)
    
    documents = relationship("Document", back_populates="owner")

class Document(Base):
    __tablename__ = "documents"

    id = Column(String(36), primary_key=True, index=True) # UUID
    filename = Column(String(255))
    upload_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(DocStatus), default=DocStatus.PROCESSING)
    doc_type = Column(Enum(DocType), default=DocType.ID_PROOF)
    confidence_score = Column(Float, default=0.0)
    file_path = Column(String(512))
    analysis_metadata = Column(JSON, nullable=True) # Stores results from 8 modules
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="documents")
    anomalies = relationship("Anomaly", back_populates="document")

class Anomaly(Base):
    __tablename__ = "anomalies"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(String(36), ForeignKey("documents.id"))
    region = Column(String(50)) # e.g., 'photo', 'text_name'
    module_source = Column(String(100)) # Which module (1-8) found this
    score = Column(Float)
    description = Column(String(255))

    document = relationship("Document", back_populates="anomalies")

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50)) # forgery, manipulation
    severity = Column(String(20)) # high, medium, low
    message = Column(String(255))
    timestamp = Column(DateTime, default=datetime.utcnow)
