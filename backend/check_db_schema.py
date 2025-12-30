import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import text, inspect

# Load .env
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(ENV_PATH)

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from app.database import engine

def check_schema():
    print("Checking 'documents' table columns:")
    inspector = inspect(engine)
    columns = inspector.get_columns('documents')
    for col in columns:
        print(f" - {col['name']} ({col['type']})")

if __name__ == "__main__":
    check_schema()
