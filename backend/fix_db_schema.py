import os
import sys
from sqlalchemy import text

# Add the parent directory to sys.path to resolve app modules
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from app.database import engine

def fix_schema():
    print("Attempting to fix database schema...")
    try:
        with engine.connect() as connection:
            # 1. doc_type
            result = connection.execute(text("SHOW COLUMNS FROM documents LIKE 'doc_type'"))
            if result.fetchone():
                print("Column 'doc_type' already exists.")
            else:
                connection.execute(text("ALTER TABLE documents ADD COLUMN doc_type ENUM('id_proof', 'certificate') DEFAULT 'id_proof'"))
                print("Successfully added 'doc_type' column.")

            # 2. analysis_metadata
            result = connection.execute(text("SHOW COLUMNS FROM documents LIKE 'analysis_metadata'"))
            if result.fetchone():
                print("Column 'analysis_metadata' already exists.")
            else:
                connection.execute(text("ALTER TABLE documents ADD COLUMN analysis_metadata JSON NULL"))
                print("Successfully added 'analysis_metadata' column.")

            # 3. confidence_score
            result = connection.execute(text("SHOW COLUMNS FROM documents LIKE 'confidence_score'"))
            if result.fetchone():
                print("Column 'confidence_score' already exists.")
            else:
                connection.execute(text("ALTER TABLE documents ADD COLUMN confidence_score FLOAT DEFAULT 0.0"))
                print("Successfully added 'confidence_score' column.")
                
            connection.commit()
    except Exception as e:
        print(f"Error updating schema: {e}")

if __name__ == "__main__":
    fix_schema()
