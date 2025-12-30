from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models import DocStatus, UserRole, DocType

# Auth
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    role: UserRole
    class Config:
        from_attributes = True

# Anomalies
class AnomalyBase(BaseModel):
    region: str
    score: float
    description: str
    module_source: Optional[str] = "General"

class Anomaly(AnomalyBase):
    id: int
    document_id: str
    class Config:
        from_attributes = True

# Documents
class DocumentBase(BaseModel):
    filename: str

class Document(DocumentBase):
    id: str
    owner_id: Optional[int] = None
    upload_date: datetime
    status: DocStatus
    doc_type: DocType
    confidence_score: float
    analysis_metadata: Optional[dict] = {}
    
    anomalies: List[Anomaly] = []

    class Config:
        from_attributes = True

class DocumentReport(Document):
    # This matches the frontend expectation specifically
    imageUrl: str
    heatmapUrl: str
    extractedFields: dict = {} # Can function as a view over analysis_metadata
    
    # We might add detailed module reports here too if the frontend wants them separately
    module_reports: Optional[dict] = {}

# Alerts
class AlertBase(BaseModel):
    type: str
    severity: str
    message: str

class Alert(AlertBase):
    id: int
    timestamp: datetime
    class Config:
        from_attributes = True
