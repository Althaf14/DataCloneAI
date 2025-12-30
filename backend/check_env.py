# backend/check_env.py
import os
from pathlib import Path
from dotenv import load_dotenv

BASE = Path(__file__).resolve().parent
ENV_PATH = BASE / ".env"
load_dotenv(ENV_PATH)

print(f"📂 Loading environment from: {ENV_PATH}")

print("DB_USER:", repr(os.getenv("DB_USER")))
print("DB_PASSWORD:", repr(os.getenv("DB_PASSWORD")))
print("DB_HOST:", repr(os.getenv("DB_HOST")))
print("DB_PORT:", repr(os.getenv("DB_PORT")))
print("DB_NAME:", repr(os.getenv("DB_NAME")))
