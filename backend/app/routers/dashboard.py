from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict
from app.database import get_db
from app.models.user import User
from app.models.document import Document
from app.models.comparison import Comparison
from app.auth.security import get_current_user, require_role

dashboard_router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@dashboard_router.get("/student")
async def get_student_dashboard(
    current_user: User = Depends(require_role(["student"])),
    db: Session = Depends(get_db)
):
    """Get student dashboard statistics."""
    # Get user's comparisons
    comparisons = db.query(Comparison).filter(
        Comparison.user_id == current_user.id
    ).all()
    
    total_comparisons = len(comparisons)
    
    if total_comparisons > 0:
        avg_similarity = sum(c.overall_similarity for c in comparisons) / total_comparisons
        high_risk_count = sum(1 for c in comparisons if c.overall_similarity >= 0.65)
    else:
        avg_similarity = 0.0
        high_risk_count = 0
    
    # Get recent comparisons
    recent_comparisons = db.query(Comparison).filter(
        Comparison.user_id == current_user.id
    ).order_by(Comparison.created_at.desc()).limit(5).all()
    
    return {
        "total_comparisons": total_comparisons,
        "average_similarity": avg_similarity,
        "high_risk_reports": high_risk_count,
        "recent_comparisons": [
            {
                "id": c.id,
                "overall_similarity": c.overall_similarity,
                "created_at": c.created_at.isoformat()
            }
            for c in recent_comparisons
        ]
    }


@dashboard_router.get("/faculty")
async def get_faculty_dashboard(
    current_user: User = Depends(require_role(["faculty", "admin"])),
    db: Session = Depends(get_db)
):
    """Get faculty dashboard statistics."""
    # Get all students
    students = db.query(User).filter(User.role == "student").all()
    total_students = len(students)
    
    # Get all comparisons
    all_comparisons = db.query(Comparison).all()
    total_comparisons = len(all_comparisons)
    
    if total_comparisons > 0:
        avg_similarity = sum(c.overall_similarity for c in all_comparisons) / total_comparisons
        high_similarity_count = sum(1 for c in all_comparisons if c.overall_similarity >= 0.65)
    else:
        avg_similarity = 0.0
        high_similarity_count = 0
    
    # Get recent comparisons
    recent_comparisons = db.query(Comparison).order_by(
        Comparison.created_at.desc()
    ).limit(10).all()
    
    recent_data = []
    for c in recent_comparisons:
        user = db.query(User).filter(User.id == c.user_id).first()
        recent_data.append({
            "id": c.id,
            "user_name": user.full_name if user else "Unknown",
            "user_email": user.email if user else "Unknown",
            "overall_similarity": c.overall_similarity,
            "created_at": c.created_at.isoformat()
        })
    
    return {
        "total_students": total_students,
        "total_comparisons": total_comparisons,
        "average_similarity": avg_similarity,
        "high_similarity_submissions": high_similarity_count,
        "recent_comparisons": recent_data
    }


@dashboard_router.get("/admin")
async def get_admin_dashboard(
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    """Get admin dashboard statistics."""
    # Get user counts
    total_users = db.query(User).count()
    students = db.query(User).filter(User.role == "student").count()
    faculty = db.query(User).filter(User.role == "faculty").count()
    admins = db.query(User).filter(User.role == "admin").count()
    
    # Get document counts
    total_documents = db.query(Document).count()
    
    # Get comparison counts
    total_comparisons = db.query(Comparison).count()
    
    if total_comparisons > 0:
        avg_similarity = db.query(func.avg(Comparison.overall_similarity)).scalar() or 0.0
    else:
        avg_similarity = 0.0
    
    # Get recent users
    recent_users = db.query(User).order_by(
        User.created_at.desc()
    ).limit(5).all()
    
    return {
        "total_users": total_users,
        "students": students,
        "faculty": faculty,
        "admins": admins,
        "total_documents": total_documents,
        "total_comparisons": total_comparisons,
        "average_similarity": avg_similarity,
        "recent_users": [
            {
                "id": u.id,
                "full_name": u.full_name,
                "email": u.email,
                "role": u.role,
                "created_at": u.created_at.isoformat()
            }
            for u in recent_users
        ]
    }
