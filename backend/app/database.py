# backend/database.py
import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load backend/.env exactly, no matter where script is run from
# Note: Assuming this file is at backend/app/database.py, we need to go up two levels to find backend/.env
# However, user code provided was: BASE_DIR = Path(__file__).resolve().parent; ENV_PATH = BASE_DIR / ".env"
# If we simply paste what user asked, it might look for .env in backend/app/.env. 
# But user said "Replace backend/database.py exactly with this". 
# Load backend/.env
# app/database.py is in backend/app/, so we go up two levels to find backend/.env
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(ENV_PATH)

# Read environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "dataclone_ai")

# Debug print to confirm loading works
print("Loaded DB Credentials:")
print("  USER:", DB_USER)
print("  PASS:", "***" if DB_PASSWORD else "(EMPTY!)")
print("  HOST:", DB_HOST)
print("  PORT:", DB_PORT)
print("  NAME:", DB_NAME)

from urllib.parse import quote_plus

# Connection URL using PyMySQL
# Quote credentials to handle special characters like '@' in password
encoded_user = quote_plus(DB_USER)
encoded_password = quote_plus(DB_PASSWORD)

DB_URL = f"mysql+pymysql://{encoded_user}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

engine = create_engine(DB_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)
Base = __import__("sqlalchemy.ext.declarative", fromlist=["declarative_base"]).declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
