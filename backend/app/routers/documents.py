from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, models, schemas, database
from typing import List, Optional
from .auth import get_current_user
import shutil
import os
import uuid
import random
from datetime import datetime

router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"]
)

from app.database import BASE_DIR

UPLOAD_DIR = BASE_DIR / "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/upload", response_model=schemas.Document)
async def upload_document(
    doc_type: str = Form("id_proof"), # Changing to str for debugging
    file: UploadFile = File(...), 
    db: Session = Depends(database.get_db), 
    current_user = Depends(get_current_user)
):
    try:
        # Generate unique ID and filename
        doc_id = str(uuid.uuid4())
        file_ext = os.path.splitext(file.filename)[1]
        saved_filename = f"{doc_id}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, saved_filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Create DB Entry
        new_doc = models.Document(
            id=doc_id,
            filename=file.filename,
            file_path=file_path,
            status=models.DocStatus.PROCESSING,
            doc_type=models.DocType(doc_type.upper()), # Validate Enum here
            owner_id=current_user.id
        )
        crud.create_document(db, new_doc)
        
        return new_doc
    except Exception as e:
        # Log error to file
        with open("backend_error.log", "a") as f:
            f.write(f"Upload Error: {str(e)}\n")
        raise HTTPException(status_code=500, detail=f"Upload Error: {str(e)}")

@router.get("/{document_id}/report", response_model=schemas.DocumentReport)
async def get_document_report(
    document_id: str,
    db: Session = Depends(database.get_db),
    current_user = Depends(get_current_user)
):
    doc = None
    if document_id == "demo":
        # Create a dummy doc object for the demo
        from collections import namedtuple
        MockDoc = namedtuple("MockDoc", ["id", "filename", "upload_date", "file_path", "doc_type"])
        doc = MockDoc(id="demo", filename="demo_sample.jpg", upload_date=datetime.utcnow(), file_path="demo_path.jpg", doc_type=models.DocType.ID_PROOF)
    else:
        doc = crud.get_document(db, document_id)
        
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Run Analysis using 8-Module System
    from app import modules
    
    # Determine full path
    if document_id == "demo":
         # Use a placeholder or real logic if we have a demo file?
         # For demo, we might skip real analysis call to avoid file not found
         analysis_results = {
             "risk_summary": {
                 "final_score": 0.98,
                 "risk_level": "LOW",
                 "breakdown": []
             },
             "pipeline_results": []
         }
         real_image_url = "https://placehold.co/800x600/png?text=Demo+Document"
    else:
         # Check if already analyzed?
         if doc.analysis_metadata:
             # Already done
             analysis_results = doc.analysis_metadata
         else:
             # Run fresh
             analysis_results = modules.analyze_document(doc.file_path, doc.doc_type)
             
             # Save to DB
             doc.analysis_metadata = analysis_results
             doc.confidence_score = analysis_results["risk_summary"]["final_score"]
             if doc.confidence_score > 0.85:
                 doc.status = models.DocStatus.VERIFIED
             else:
                 doc.status = models.DocStatus.FLAGGED
                 
             # Save anomalies
             for res in analysis_results.get("pipeline_results", []):
                 for anom in res.get("anomalies", []):
                     db_anom = models.Anomaly(
                         document_id=doc.id,
                         region=anom.get("region", "unknown"),
                         module_source=res.get("module", "General"),
                         score=anom.get("score", 0.0),
                         description=anom.get("description", "Issue detected")
                     )
                     db.add(db_anom)
             
             db.commit()
             db.refresh(doc)
         
         real_image_url = f"http://127.0.0.1:8000/uploads/{os.path.basename(doc.file_path)}"
    
    # Construct Response
    risk_data = analysis_results.get("risk_summary", {})
    
    anomalies_list = []
    if document_id != "demo":
         # Reload from DB to get IDs etc if needed, or just map from pipeline results
         # Mapping from pipeline results for immediate feedback
         for res in analysis_results.get("pipeline_results", []):
             for anom in res.get("anomalies", []):
                 anomalies_list.append(
                     schemas.Anomaly(
                         id=0, # Placeholder
                         document_id=doc.id,
                         region=anom.get("region", "unknown"),
                         score=anom.get("score", 0.0),
                         description=anom.get("description", ""),
                         module_source=res.get("module", "General")
                     )
                 )
    
    # Extract Heatmap from Visual Forgery Module
    heatmap_url = "https://placehold.co/800x600/png?text=No+Heatmap+Available"
    vf_res = next((res for res in analysis_results.get("pipeline_results", []) if "Visual Forgery" in res.get("module", "")), None)
    if vf_res and "heatmap_b64" in vf_res.get("metadata", {}):
        heatmap_url = vf_res["metadata"]["heatmap_b64"]

    # Normalize Confidence Score (0-100 -> 0.0-1.0) for Frontend Compatibility
    raw_score = doc.confidence_score if hasattr(doc, 'confidence_score') else 0.98
    normalized_score = raw_score / 100.0 if raw_score > 1.0 else raw_score

    response = schemas.DocumentReport(
        id=doc.id,
        filename=doc.filename,
        upload_date=doc.upload_date,
        status=doc.status if hasattr(doc, 'status') else models.DocStatus.PROCESSING,
        doc_type=doc.doc_type if hasattr(doc, 'doc_type') else models.DocType.ID_PROOF,
        confidence_score=normalized_score,
        anomalies=anomalies_list,
        imageUrl=real_image_url, 
        heatmapUrl=heatmap_url,
        extractedFields=next((res.get("metadata", {}) for res in analysis_results.get("pipeline_results", []) if "OCR" in res.get("module", "")), {}) if document_id != "demo" else {},
        module_reports={"raw": analysis_results}
    )
    
    return response

@router.get("/", response_model=List[schemas.Document])
def read_documents(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(database.get_db),
    current_user = Depends(get_current_user)
):
    docs = crud.get_documents_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return docs

@router.get("/{document_id}", response_model=schemas.Document)
async def get_document_details(
    document_id: str, 
    db: Session = Depends(database.get_db),
    current_user = Depends(get_current_user)
):
    doc = crud.get_document(db, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc
