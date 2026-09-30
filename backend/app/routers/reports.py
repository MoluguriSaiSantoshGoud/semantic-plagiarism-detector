from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pathlib import Path
from app.database import get_db
from app.models.user import User
from app.models.comparison import Comparison
from app.models.report import Report
from app.schemas.report import ReportResponse
from app.auth.security import get_current_user
from app.services.report_generator import ReportGenerator
from app.config import settings

reports_router = APIRouter(prefix="/api/reports", tags=["Reports"])
report_generator = ReportGenerator()


@reports_router.get("/{comparison_id}", response_model=ReportResponse)
async def get_report(
    comparison_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get report information for a comparison."""
    # Check if comparison exists and belongs to user
    comparison = db.query(Comparison).filter(
        Comparison.id == comparison_id,
        Comparison.user_id == current_user.id
    ).first()
    
    if not comparison:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comparison not found"
        )
    
    # Check if report exists
    report = db.query(Report).filter(Report.comparison_id == comparison_id).first()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    return report


@reports_router.get("/{comparison_id}/download")
async def download_report(
    comparison_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Download PDF report for a comparison."""
    # Check if comparison exists and belongs to user
    comparison = db.query(Comparison).filter(
        Comparison.id == comparison_id,
        Comparison.user_id == current_user.id
    ).first()
    
    if not comparison:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comparison not found"
        )
    
    # Check if report exists
    report = db.query(Report).filter(Report.comparison_id == comparison_id).first()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found. Generate report first."
        )
    
    # Check if file exists
    report_path = Path(report.report_path)
    if not report_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report file not found"
        )
    
    return FileResponse(
        path=report_path,
        filename=f"plagiarism_report_{comparison_id}.pdf",
        media_type="application/pdf"
    )


@reports_router.post("/{comparison_id}/generate", response_model=ReportResponse)
async def generate_report(
    comparison_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate PDF report for a comparison."""
    # Check if comparison exists and belongs to user
    comparison = db.query(Comparison).filter(
        Comparison.id == comparison_id,
        Comparison.user_id == current_user.id
    ).first()
    
    if not comparison:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comparison not found"
        )
    
    # Check if report already exists
    existing_report = db.query(Report).filter(Report.comparison_id == comparison_id).first()
    if existing_report:
        return existing_report
    
    # Get comparison details
    from app.routers.comparisons import comparisons_router
    from app.models.document import Document, DocumentChunk
    from app.models.comparison import Match
    
    ref_doc = db.query(Document).filter(Document.id == comparison.reference_document_id).first()
    sub_doc = db.query(Document).filter(Document.id == comparison.submitted_document_id).first()
    
    matches = db.query(Match).filter(Match.comparison_id == comparison_id).all()
    
    # Build comparison data for report
    match_data = []
    for match in matches:
        ref_chunk = db.query(DocumentChunk).filter(DocumentChunk.id == match.reference_chunk_id).first()
        sub_chunk = db.query(DocumentChunk).filter(DocumentChunk.id == match.submitted_chunk_id).first()
        
        match_data.append({
            "reference_chunk": {
                "text": ref_chunk.text if ref_chunk else "",
                "word_count": ref_chunk.word_count if ref_chunk else 0
            },
            "submitted_chunk": {
                "text": sub_chunk.text if sub_chunk else "",
                "word_count": sub_chunk.word_count if sub_chunk else 0
            },
            "semantic_score": match.semantic_score,
            "lexical_score": match.lexical_score,
            "ngram_score": match.ngram_score,
            "exact_match_score": match.exact_match_score,
            "combined_score": match.combined_score,
            "classification": match.classification,
            "explanation": match.explanation
        })
    
    comparison_data = {
        "id": comparison.id,
        "reference_filename": ref_doc.filename if ref_doc else "Unknown",
        "submitted_filename": sub_doc.filename if sub_doc else "Unknown",
        "overall_similarity": comparison.overall_similarity,
        "weighted_similarity": comparison.weighted_similarity,
        "processing_time": comparison.processing_time,
        "matches": match_data,
        "statistics": {
            "total_submitted_chunks": len(sub_doc.chunks) if sub_doc else 0,
            "matching_chunk_count": len(match_data),
            "very_high_similarity_chunk_count": sum(1 for m in match_data if m["combined_score"] >= 0.80),
            "high_similarity_chunk_count": sum(1 for m in match_data if 0.65 <= m["combined_score"] < 0.80),
            "moderate_similarity_chunk_count": sum(1 for m in match_data if 0.45 <= m["combined_score"] < 0.65),
            "low_similarity_chunk_count": sum(1 for m in match_data if m["combined_score"] < 0.45),
        }
    }
    
    # Generate report file path
    report_dir = Path(settings.report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    report_filename = f"report_{comparison.id}_{int(__import__('time').time())}.pdf"
    report_path = report_dir / report_filename
    
    # Generate PDF
    try:
        generated_path = report_generator.generate_report(
            comparison_data,
            current_user.full_name,
            str(report_path)
        )
        
        # Create report record
        report = Report(
            comparison_id=comparison.id,
            report_path=generated_path
        )
        
        db.add(report)
        db.commit()
        db.refresh(report)
        
        return report
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Report generation failed: {str(e)}"
        )
