import os
import sys
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

def fix_data():
    print(f"Connecting to {DB_URL}...")
    try:
        engine = create_engine(DB_URL)
        with engine.connect() as connection:
            print("Connected. Updating existing data to uppercase...")
            
            # Update lowercase to uppercase
            # We assume the column is already ENUM('ID_PROOF', 'CERTIFICATE') from previous step, 
            # or arguably it might be in a state where it allows both? 
            # If strictly ENUM uppercase, lowercase data might be invalid index 0 or similar?
            # Actually, MySQL ENUM is case-insensitive for storage usually, but SQLAlchemy validation is strict Python side.
            # But just to be sure, we run UPPDATE.
            
            # Note: If the column is strictly ENUM('ID_PROOF'), then 'id_proof' might already be normalized OR 
            # if we changed the definition, it might have mapped to index.
            
            # Let's try explicit update.
            # Convert 'id_proof' -> 'ID_PROOF'
            sql = "UPDATE documents SET doc_type = UPPER(doc_type)"
            result = connection.execute(text(sql))
            print(f"Updated records. Rows matched: {result.rowcount}")
            
            connection.commit()
    except Exception as e:
        print(f"Fatal error: {e}")

if __name__ == "__main__":
    fix_data()
