import os
import aiofiles
from pathlib import Path
from typing import Optional
from fastapi import UploadFile, HTTPException
from app.config import settings


ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain"
}


def get_file_extension(filename: str) -> str:
    return Path(filename).suffix.lower()


def validate_file_type(file: UploadFile) -> bool:
    extension = get_file_extension(file.filename)
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type {extension} not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Validate file size
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Seek back to start
    
    max_size = settings.max_file_size_mb * 1024 * 1024
    if file_size > max_size:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum allowed size of {settings.max_file_size_mb}MB"
        )
    
    return True


async def save_uploaded_file(file: UploadFile, user_id: int) -> str:
    # Create upload directory if it doesn't exist
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Create user-specific directory
    user_dir = upload_dir / str(user_id)
    user_dir.mkdir(exist_ok=True)
    
    # Generate unique filename
    extension = get_file_extension(file.filename)
    timestamp = str(int(__import__("time").time()))
    filename = f"{timestamp}_{file.filename}"
    file_path = user_dir / filename
    
    # Save file
    async with aiofiles.open(file_path, "wb") as f:
        content = await file.read()
        await f.write(content)
    
    return str(file_path)
