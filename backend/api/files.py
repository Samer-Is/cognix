"""
File upload API endpoints for RAG
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
import logging
import os

from database.connection import get_db
from database.models import User, UploadedFile
from database.schemas import FileUploadResponse, FileListResponse
from api.auth import get_current_user
from services.rag_service import RAGService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Upload file for RAG processing"""
    
    # Validate file type
    allowed_types = ["pdf", "docx", "csv", "txt"]
    file_ext = file.filename.split(".")[-1].lower()
    
    if file_ext not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"File type .{file_ext} not supported. Allowed: {', '.join(allowed_types)}"
        )
    
    try:
        # Read file content
        content = await file.read()
        file_size = len(content)
        
        # Initialize RAG service
        rag_service = RAGService()
        
        # Upload to S3 and process
        s3_key = await rag_service.upload_file(
            file_content=content,
            filename=file.filename,
            user_id=current_user.id
        )
        
        # Create database record
        uploaded_file = UploadedFile(
            user_id=current_user.id,
            filename=file.filename,
            file_type=file_ext,
            file_size=file_size,
            s3_key=s3_key,
            status="processing"
        )
        
        db.add(uploaded_file)
        await db.commit()
        await db.refresh(uploaded_file)
        
        # Process file in background (this would be async)
        # await rag_service.process_file(uploaded_file.id)
        
        logger.info(f"File uploaded: {file.filename} by user {current_user.username}")
        
        return FileUploadResponse(
            file_id=uploaded_file.id,
            filename=file.filename,
            file_type=file_ext,
            file_size=file_size,
            status="processing",
            message="File uploaded successfully and is being processed"
        )
        
    except Exception as e:
        logger.error(f"File upload error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")


@router.get("/list", response_model=FileListResponse)
async def list_files(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all uploaded files for current user"""
    
    from sqlalchemy import select
    
    result = await db.execute(
        select(UploadedFile)
        .filter(UploadedFile.user_id == current_user.id)
        .order_by(UploadedFile.created_at.desc())
    )
    files = result.scalars().all()
    
    file_list = [
        {
            "id": f.id,
            "filename": f.filename,
            "file_type": f.file_type,
            "file_size": f.file_size,
            "status": f.status,
            "created_at": f.created_at
        }
        for f in files
    ]
    
    return FileListResponse(files=file_list)


@router.delete("/{file_id}")
async def delete_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete uploaded file"""
    
    from sqlalchemy import select, delete
    
    result = await db.execute(
        select(UploadedFile).filter(
            UploadedFile.id == file_id,
            UploadedFile.user_id == current_user.id
        )
    )
    file = result.scalar_one_or_none()
    
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Delete from S3
    rag_service = RAGService()
    await rag_service.delete_file(file.s3_key)
    
    # Delete from database
    await db.execute(
        delete(UploadedFile).filter(UploadedFile.id == file_id)
    )
    await db.commit()
    
    logger.info(f"File deleted: {file.filename}")
    
    return {"message": "File deleted successfully"}
