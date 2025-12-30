import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

# Load .env
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(ENV_PATH)

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "dataclone_ai")

encoded_user = quote_plus(DB_USER)
encoded_password = quote_plus(DB_PASSWORD)

DB_URL = f"mysql+pymysql://{encoded_user}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

def fix():
    print(f"Connecting to {DB_URL}...")
    try:
        engine = create_engine(DB_URL)
        with engine.connect() as connection:
            print("Connected.")
            
            # 1. doc_type
            try:
                connection.execute(text("ALTER TABLE documents ADD COLUMN doc_type ENUM('id_proof', 'certificate') DEFAULT 'id_proof'"))
                print("Added doc_type")
            except Exception as e:
                print(f"doc_type might exist: {e}")

            # 2. analysis_metadata
            try:
                connection.execute(text("ALTER TABLE documents ADD COLUMN analysis_metadata JSON NULL"))
                print("Added analysis_metadata")
            except Exception as e:
                print(f"analysis_metadata might exist: {e}")

            # 3. confidence_score
            try:
                connection.execute(text("ALTER TABLE documents ADD COLUMN confidence_score FLOAT DEFAULT 0.0"))
                print("Added confidence_score")
            except Exception as e:
                print(f"confidence_score might exist: {e}")
                
            connection.commit()
            print("Changes committed.")
    except Exception as e:
        print(f"Fatal error: {e}")

if __name__ == "__main__":
    fix()
