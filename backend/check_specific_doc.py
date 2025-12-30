import sys
import os
from sqlalchemy.orm import Session
from app import models, database

# Add parent dir to path
sys.path.append(os.getcwd())

def check_doc():
    doc_id = "7b23de96-9c05-4766-810d-f75e119c7bc7"
    print(f"Checking for document: {doc_id}")
    db = database.SessionLocal()
    try:
        doc = db.query(models.Document).filter(models.Document.id == doc_id).first()
        if doc:
            print(f"FOUND: {doc.filename} ({doc.doc_type})")
        else:
            print("NOT FOUND")
    except Exception as e:
        print(f"DB Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_doc()
