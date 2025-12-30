import sys
import os
from sqlalchemy.orm import Session
from app import models, database, modules

# Add parent dir to path
sys.path.append(os.getcwd())

def test_analysis():
    doc_id = "7b23de96-9c05-4766-810d-f75e119c7bc7"
    print(f"Testing analysis for: {doc_id}")
    
    db = database.SessionLocal()
    try:
        doc = db.query(models.Document).filter(models.Document.id == doc_id).first()
        if not doc:
            print("Doc not found!")
            return

        print(f"Running analyze_document('{doc.file_path}', '{doc.doc_type}')...")
        try:
            results = modules.analyze_document(doc.file_path, doc.doc_type)
            print("Analysis SUCCESS!")
            print(results)
        except Exception as e:
            print(f"Analysis FAILED: {e}")
            import traceback
            traceback.print_exc()

    except Exception as e:
        print(f"DB Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_analysis()
