import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect
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

def check_docs():
    print(f"Connecting to {DB_URL}...")
    engine = create_engine(DB_URL)
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns('documents')]
    print(f"Columns in 'documents': {columns}")
    
    if 'analysis_metadata' not in columns:
        print("MISSING: analysis_metadata")
    else:
        print("FOUND: analysis_metadata")

if __name__ == "__main__":
    check_docs()
