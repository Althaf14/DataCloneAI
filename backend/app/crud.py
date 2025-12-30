from sqlalchemy.orm import Session
from . import models, schemas
import bcrypt
from typing import List

# pwd_context removed

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def verify_password(plain_password, hashed_password):
    # bcrypt.checkpw expects bytes
    password_byte_enc = plain_password.encode('utf-8')
    hashed_password_byte_enc = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_byte_enc, hashed_password_byte_enc)

def get_hash_password(password):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_password.decode('utf-8')

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_hash_password(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_alerts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Alert).offset(skip).limit(limit).all()

def create_alert(db: Session, alert: schemas.AlertBase):
    db_alert = models.Alert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

def get_document(db: Session, document_id: str):
    return db.query(models.Document).filter(models.Document.id == document_id).first()

def create_document(db: Session, document: models.Document):
    db.add(document)
    db.commit()
    db.refresh(document)
    return document

def get_documents_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Document).filter(models.Document.owner_id == user_id).offset(skip).limit(limit).all()
