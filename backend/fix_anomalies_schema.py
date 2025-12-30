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

def fix_anomalies():
    print(f"Connecting to {DB_URL}...")
    try:
        engine = create_engine(DB_URL)
        with engine.connect() as connection:
            print("Connected. Checking anomalies table...")
            
            # Check module_source
            try:
                connection.execute(text("ALTER TABLE anomalies ADD COLUMN module_source VARCHAR(50)"))
                print("Added module_source column.")
            except Exception as e:
                print(f"module_source might exist: {e}")

            # Check region (seen in query)
            try:
                connection.execute(text("ALTER TABLE anomalies ADD COLUMN region JSON"))
                print("Added region column.")
            except Exception as e:
                print(f"region might exist: {e}")

            # Check score (seen in query)
            try:
                connection.execute(text("ALTER TABLE anomalies ADD COLUMN score FLOAT"))
                print("Added score column.")
            except Exception as e:
                print(f"score might exist: {e}")

            # Check description (seen in query)
            try:
                connection.execute(text("ALTER TABLE anomalies ADD COLUMN description TEXT"))
                print("Added description column.")
            except Exception as e:
                print(f"description might exist: {e}")

            connection.commit()
            print("Anomalies schema update committed.")
    except Exception as e:
        print(f"Fatal error: {e}")

if __name__ == "__main__":
    fix_anomalies()
