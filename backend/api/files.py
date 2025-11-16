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
        
        # Process file immediately
        process_result = await rag_service.process_file(file.filename, content)
        
        if "error" in process_result:
            raise HTTPException(status_code=400, detail=process_result["error"])
        
        # Upload to S3 (optional, for backup)
        try:
            s3_key = await rag_service.upload_file(
                file_content=content,
                filename=file.filename,
                user_id=current_user.id
            )
        except Exception as e:
            logger.warning(f"S3 upload failed (continuing anyway): {e}")
            s3_key = f"local/{file.filename}"  # Fallback key
        
        # Create database record
        uploaded_file = UploadedFile(
            user_id=current_user.id,
            filename=file.filename,
            file_type=file_ext,
            file_size=file_size,
            s3_key=s3_key,
            status="ready",  # Changed from "processing" since we process immediately
            num_chunks=process_result.get("chunks_processed", 0),
            embedding_status="completed"
        )
        
        db.add(uploaded_file)
        await db.commit()
        await db.refresh(uploaded_file)
        
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


@router.post("/search")
async def search_documents(
    query: str,
    top_k: int = 5,
    current_user: User = Depends(get_current_user)
):
    """Search through uploaded documents"""
    
    rag_service = RAGService()
    results = await rag_service.search_documents(query, top_k=top_k)
    
    return {
        "query": query,
        "results": results,
        "count": len(results)
    }


@router.get("/stats")
async def get_rag_stats(
    current_user: User = Depends(get_current_user)
):
    """Get RAG vector store statistics"""
    
    rag_service = RAGService()
    stats = rag_service.get_vector_store_stats()
    
    return stats


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
    
    # Delete from S3 (if it was uploaded)
    try:
        rag_service = RAGService()
        await rag_service.delete_file(file.s3_key)
    except Exception as e:
        logger.warning(f"S3 delete failed (continuing anyway): {e}")
    
    # Delete from database
    await db.execute(
        delete(UploadedFile).filter(UploadedFile.id == file_id)
    )
    await db.commit()
    
    logger.info(f"File deleted: {file.filename}")
    
    return {"message": "File deleted successfully"}
