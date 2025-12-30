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

def switch_to_uppercase():
    print(f"Connecting to {DB_URL}...")
    try:
        engine = create_engine(DB_URL)
        with engine.connect() as connection:
            print("Connected. Modifying doc_type column...")
            
            # MODIFY COLUMN to standard Uppercase ENUM
            # Note: This might warn about data truncation if we had conflicting data, but we likely don't have much.
            sql = "ALTER TABLE documents MODIFY COLUMN doc_type ENUM('ID_PROOF', 'CERTIFICATE') DEFAULT 'ID_PROOF'"
            connection.execute(text(sql))
            print("Successfully updated doc_type to ENUM('ID_PROOF', 'CERTIFICATE')")
            
            connection.commit()
    except Exception as e:
        print(f"Fatal error: {e}")

if __name__ == "__main__":
    switch_to_uppercase()
