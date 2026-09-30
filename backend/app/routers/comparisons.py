from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.document import Document, DocumentChunk
from app.models.comparison import Comparison, Match
from app.schemas.comparison import ComparisonCreate, ComparisonResponse, ComparisonDetailedResponse
from app.auth.security import get_current_user
from app.services.document_processor import DocumentProcessor
from app.services.plagiarism import PlagiarismDetector
from app.services.report_generator import ReportGenerator

comparisons_router = APIRouter(prefix="/api/comparisons", tags=["Comparisons"])
document_processor = DocumentProcessor()
plagiarism_detector = PlagiarismDetector()
report_generator = ReportGenerator()


@comparisons_router.post("", response_model=ComparisonResponse)
async def create_comparison(
    comparison_data: ComparisonCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Compare two texts for plagiarism."""
    # Validate inputs
    if not comparison_data.reference_text or not comparison_data.reference_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reference text cannot be empty"
        )
    
    if not comparison_data.submitted_text or not comparison_data.submitted_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Submitted text cannot be empty"
        )
    
    try:
        # Process reference text
        ref_data = document_processor.process_text_input(comparison_data.reference_text)
        if "error" in ref_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ref_data["error"]
            )
        
        # Process submitted text
        sub_data = document_processor.process_text_input(comparison_data.submitted_text)
        if "error" in sub_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=sub_data["error"]
            )
        
        # Create reference document record
        ref_document = Document(
            user_id=current_user.id,
            filename=comparison_data.reference_filename,
            file_type="txt",
            storage_path="",
            extracted_text=ref_data["full_text"],
            page_count=ref_data["page_count"],
            word_count=ref_data["word_count"]
        )
        db.add(ref_document)
        db.commit()
        db.refresh(ref_document)
        
        # Create reference chunks
        for chunk_data in ref_data["chunks"]:
            chunk = DocumentChunk(
                document_id=ref_document.id,
                chunk_index=chunk_data["chunk_index"],
                paragraph_index=chunk_data["paragraph_index"],
                page_number=chunk_data["page_number"],
                text=chunk_data["text"],
                word_count=chunk_data["word_count"]
            )
            db.add(chunk)
        db.commit()
        
        # Create submitted document record
        sub_document = Document(
            user_id=current_user.id,
            filename=comparison_data.submitted_filename,
            file_type="txt",
            storage_path="",
            extracted_text=sub_data["full_text"],
            page_count=sub_data["page_count"],
            word_count=sub_data["word_count"]
        )
        db.add(sub_document)
        db.commit()
        db.refresh(sub_document)
        
        # Create submitted chunks
        for chunk_data in sub_data["chunks"]:
            chunk = DocumentChunk(
                document_id=sub_document.id,
                chunk_index=chunk_data["chunk_index"],
                paragraph_index=chunk_data["paragraph_index"],
                page_number=chunk_data["page_number"],
                text=chunk_data["text"],
                word_count=chunk_data["word_count"]
            )
            db.add(chunk)
        db.commit()
        
        # Perform comparison
        comparison_result = plagiarism_detector.compare_documents(
            ref_data["chunks"],
            sub_data["chunks"]
        )
        
        # Create comparison record
        comparison = Comparison(
            user_id=current_user.id,
            reference_document_id=ref_document.id,
            submitted_document_id=sub_document.id,
            overall_similarity=comparison_result["overall_similarity"],
            weighted_similarity=comparison_result["weighted_similarity"],
            processing_time=comparison_result["processing_time"]
        )
        db.add(comparison)
        db.commit()
        db.refresh(comparison)
        
        # Create match records
        for match_data in comparison_result["matches"]:
            # Get chunk IDs
            ref_chunk = db.query(DocumentChunk).filter(
                DocumentChunk.document_id == ref_document.id,
                DocumentChunk.chunk_index == match_data["reference_chunk_id"]
            ).first()
            
            sub_chunk = db.query(DocumentChunk).filter(
                DocumentChunk.document_id == sub_document.id,
                DocumentChunk.chunk_index == match_data["submitted_chunk_id"]
            ).first()
            
            if ref_chunk and sub_chunk:
                match = Match(
                    comparison_id=comparison.id,
                    reference_chunk_id=ref_chunk.id,
                    submitted_chunk_id=sub_chunk.id,
                    semantic_score=match_data["semantic_score"],
                    lexical_score=match_data["lexical_score"],
                    ngram_score=match_data["ngram_score"],
                    exact_match_score=match_data["exact_match_score"],
                    combined_score=match_data["combined_score"],
                    classification=match_data["classification"],
                    explanation=match_data["explanation"]
                )
                db.add(match)
        
        db.commit()
        db.refresh(comparison)
        
        return comparison
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Comparison failed: {str(e)}"
        )


@comparisons_router.get("", response_model=List[ComparisonResponse])
async def get_comparisons(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's comparisons."""
    query = db.query(Comparison).filter(Comparison.user_id == current_user.id)
    comparisons = query.order_by(Comparison.created_at.desc()).offset(skip).limit(limit).all()
    return comparisons


@comparisons_router.get("/{comparison_id}", response_model=ComparisonDetailedResponse)
async def get_comparison(
    comparison_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific comparison with full details."""
    comparison = db.query(Comparison).filter(
        Comparison.id == comparison_id,
        Comparison.user_id == current_user.id
    ).first()
    
    if not comparison:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comparison not found"
        )
    
    # Get documents
    ref_doc = db.query(Document).filter(Document.id == comparison.reference_document_id).first()
    sub_doc = db.query(Document).filter(Document.id == comparison.submitted_document_id).first()
    
    # Get matches with chunk details
    matches = db.query(Match).filter(Match.comparison_id == comparison.id).all()
    
    # Build match responses with chunk text
    match_responses = []
    for match in matches:
        ref_chunk = db.query(DocumentChunk).filter(DocumentChunk.id == match.reference_chunk_id).first()
        sub_chunk = db.query(DocumentChunk).filter(DocumentChunk.id == match.submitted_chunk_id).first()
        
        match_responses.append({
            "id": match.id,
            "reference_chunk_id": match.reference_chunk_id,
            "submitted_chunk_id": match.submitted_chunk_id,
            "semantic_score": match.semantic_score,
            "lexical_score": match.lexical_score,
            "ngram_score": match.ngram_score,
            "exact_match_score": match.exact_match_score,
            "combined_score": match.combined_score,
            "classification": match.classification,
            "explanation": match.explanation,
            "reference_text": ref_chunk.text if ref_chunk else "",
            "submitted_text": sub_chunk.text if sub_chunk else ""
        })
    
    # Calculate statistics
    stats = {
        "total_reference_chunks": len(ref_doc.chunks) if ref_doc else 0,
        "total_submitted_chunks": len(sub_doc.chunks) if sub_doc else 0,
        "matching_chunk_count": len(match_responses),
        "very_high_similarity_chunk_count": sum(1 for m in match_responses if m["combined_score"] >= 0.80),
        "high_similarity_chunk_count": sum(1 for m in match_responses if 0.65 <= m["combined_score"] < 0.80),
        "moderate_similarity_chunk_count": sum(1 for m in match_responses if 0.45 <= m["combined_score"] < 0.65),
        "low_similarity_chunk_count": sum(1 for m in match_responses if m["combined_score"] < 0.45),
    }
    
    return ComparisonDetailedResponse(
        id=comparison.id,
        overall_similarity=comparison.overall_similarity,
        weighted_similarity=comparison.weighted_similarity,
        processing_time=comparison.processing_time,
        created_at=comparison.created_at,
        reference_document={
            "id": ref_doc.id,
            "filename": ref_doc.filename,
            "word_count": ref_doc.word_count
        } if ref_doc else {},
        submitted_document={
            "id": sub_doc.id,
            "filename": sub_doc.filename,
            "word_count": sub_doc.word_count
        } if sub_doc else {},
        matches=match_responses,
        statistics=stats
    )


@comparisons_router.delete("/{comparison_id}")
async def delete_comparison(
    comparison_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a comparison."""
    comparison = db.query(Comparison).filter(
        Comparison.id == comparison_id,
        Comparison.user_id == current_user.id
    ).first()
    
    if not comparison:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comparison not found"
        )
    
    db.delete(comparison)
    db.commit()
    
    return {"message": "Comparison deleted successfully"}
