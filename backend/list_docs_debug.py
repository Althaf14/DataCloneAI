import sys
import os
from sqlalchemy.orm import Session
from app import models, database

sys.path.append(os.getcwd())

def list_docs():
    db = database.SessionLocal()
    try:
        docs = db.query(models.Document).all()
        print(f"Found {len(docs)} documents:")
        for doc in docs:
            print(f"- ID: {doc.id} | Filename: {doc.filename} | Status: {doc.status}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    list_docs()
