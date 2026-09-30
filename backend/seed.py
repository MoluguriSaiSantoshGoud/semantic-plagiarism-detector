"""
Seed script to create initial users and sample data.
Run this script after setting up the database to create default accounts.
"""

from app.database import SessionLocal, Base, engine
from app.models.user import User
import hashlib


def get_password_hash(password: str) -> str:
    """Simple password hashing using SHA-256 for seed script."""
    return hashlib.sha256(password.encode()).hexdigest()


def seed_database():
    """Create initial users and sample data."""
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if users already exist
        existing_users = db.query(User).count()
        if existing_users > 0:
            print("Database already seeded. Skipping...")
            return
        
        # Create student user
        student = User(
            full_name="Student User",
            email="student@example.com",
            password_hash=get_password_hash("password123"),
            role="student",
            is_active=True
        )
        db.add(student)
        
        # Create faculty user
        faculty = User(
            full_name="Faculty User",
            email="faculty@example.com",
            password_hash=get_password_hash("password123"),
            role="faculty",
            is_active=True
        )
        db.add(faculty)
        
        # Create admin user
        admin = User(
            full_name="Admin User",
            email="admin@example.com",
            password_hash=get_password_hash("password123"),
            role="admin",
            is_active=True
        )
        db.add(admin)
        
        db.commit()
        
        print("Database seeded successfully!")
        print("\nDefault accounts created:")
        print("Student:  student@example.com / password123")
        print("Faculty:  faculty@example.com / password123")
        print("Admin:    admin@example.com / password123")
        print("\nIMPORTANT: Change these passwords in production!")
        
    except Exception as e:
        print(f"Error seeding database: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
