import sys
import os
from sqlalchemy.orm import Session
from app import models, database

# Add parent dir to path
sys.path.append(os.getcwd())

def verify_read():
    print("Testing database read...")
    db = database.SessionLocal()
    try:
        # Try to read documents
        docs = db.query(models.Document).limit(5).all()
        print(f"Successfully read {len(docs)} documents.")
        for d in docs:
            print(f" - {d.filename} ({d.doc_type})")
        print("Backend read verification PASSED.")
    except Exception as e:
        print(f"Backend read verification FAILED: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    verify_read()
