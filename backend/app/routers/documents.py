from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from pathlib import Path
from app.database import get_db
from app.models.user import User
from app.models.document import Document, DocumentChunk
from app.schemas.document import DocumentResponse
from app.auth.security import get_current_user
from app.services.document_processor import DocumentProcessor
from app.utils.file_handler import validate_file_type, save_uploaded_file
from app.config import settings

documents_router = APIRouter(prefix="/api/documents", tags=["Documents"])
document_processor = DocumentProcessor()


@documents_router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload and process a document."""
    # Validate file type
    validate_file_type(file)
    
    # Save file
    file_path = await save_uploaded_file(file, current_user.id)
    
    # Determine file type
    file_extension = Path(file.filename).suffix.lower()
    file_type = file_extension[1:]  # Remove the dot
    
    try:
        # Extract text and process document
        extracted_data = document_processor.extract_text(file_path, file_type)
        
        if "error" in extracted_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=extracted_data["error"]
            )
        
        # Create document record
        document = Document(
            user_id=current_user.id,
            filename=file.filename,
            file_type=file_type,
            storage_path=file_path,
            extracted_text=extracted_data["full_text"],
            page_count=extracted_data["page_count"],
            word_count=extracted_data["word_count"]
        )
        
        db.add(document)
        db.commit()
        db.refresh(document)
        
        # Create chunks
        for chunk_data in extracted_data["chunks"]:
            chunk = DocumentChunk(
                document_id=document.id,
                chunk_index=chunk_data["chunk_index"],
                paragraph_index=chunk_data["paragraph_index"],
                page_number=chunk_data["page_number"],
                text=chunk_data["text"],
                word_count=chunk_data["word_count"]
            )
            db.add(chunk)
        
        db.commit()
        db.refresh(document)
        
        return document
        
    except Exception as e:
        # Cleanup on error
        if Path(file_path).exists():
            Path(file_path).unlink()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document processing failed: {str(e)}"
        )


@documents_router.get("", response_model=List[DocumentResponse])
async def get_documents(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's documents."""
    query = db.query(Document).filter(Document.user_id == current_user.id)
    documents = query.order_by(Document.uploaded_at.desc()).offset(skip).limit(limit).all()
    return documents


@documents_router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific document."""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    return document


@documents_router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a document."""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Delete file from storage
    file_path = Path(document.storage_path)
    if file_path.exists():
        file_path.unlink()
    
    # Delete from database (cascade will delete chunks)
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted successfully"}
