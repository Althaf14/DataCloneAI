from sqlalchemy import create_engine
from app.database import Base, engine, SessionLocal
from app.models import User, UserRole
from passlib.context import CryptContext

# Basic hashing for seed
pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

def init_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Check if admin exists
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        print("Creating admin user...")
        hashed_pw = pwd_context.hash("password")
        admin_user = User(
            username="admin", 
            hashed_password=hashed_pw,
            role=UserRole.ADMIN
        )
        db.add(admin_user)
        db.commit()
        print("Admin user created (admin/password)")
    else:
        print("Admin user already exists.")
    
    db.close()

if __name__ == "__main__":
    print("Initializing Database...")
    try:
        init_db()
        print("Database initialization complete.")
    except Exception as e:
        print(f"Error initializing database: {e}")
