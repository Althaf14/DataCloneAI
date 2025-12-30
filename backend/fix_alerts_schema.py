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

def fix_alerts():
    print(f"Connecting to {DB_URL}...")
    try:
        engine = create_engine(DB_URL)
        with engine.connect() as connection:
            print("Connected. Checking alerts table...")
            
            # Check type
            try:
                connection.execute(text("ALTER TABLE alerts ADD COLUMN type VARCHAR(50)"))
                print("Added type column.")
            except Exception as e:
                print(f"type might exist: {e}")

            # Check severity
            try:
                connection.execute(text("ALTER TABLE alerts ADD COLUMN severity VARCHAR(20)"))
                print("Added severity column.")
            except Exception as e:
                print(f"severity might exist: {e}")

            # Check message
            try:
                connection.execute(text("ALTER TABLE alerts ADD COLUMN message VARCHAR(255)"))
                print("Added message column.")
            except Exception as e:
                print(f"message might exist: {e}")

            # Check timestamp
            try:
                connection.execute(text("ALTER TABLE alerts ADD COLUMN timestamp DATETIME DEFAULT CURRENT_TIMESTAMP"))
                print("Added timestamp column.")
            except Exception as e:
                print(f"timestamp might exist: {e}")

            connection.commit()
            print("Alerts schema update committed.")
    except Exception as e:
        print(f"Fatal error: {e}")

if __name__ == "__main__":
    fix_alerts()
