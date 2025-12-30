from fastapi import FastAPI # Reload Trigger
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, documents, alerts
from .database import engine, Base

# Create tables on startup (simplest migration strategy)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DataClone AI API",
    description="Backend for Identity Forgery Detection System",
    version="1.0.0"
)

# CORS
origins = [
    "http://localhost:5173", # Vite Dev Server
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(alerts.router)

from fastapi.staticfiles import StaticFiles
import os
from .database import BASE_DIR

UPLOAD_DIR = BASE_DIR / "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

@app.get("/")
def read_root():
    return {"message": "Welcome to DataClone AI Backend"}
