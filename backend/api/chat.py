"""
Chat API endpoints with AI agents
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import logging
import time
import uuid

from database.connection import get_db
from database.models import User, Conversation, ActivityLog
from database.schemas import ChatRequest, ChatResponse, AgentLog, MessageRole
from api.auth import get_current_user
from agents.orchestrator import AgentOrchestrator

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Main chat endpoint with AI agents"""
    
    start_time = time.time()
    session_id = request.session_id or str(uuid.uuid4())
    
    try:
        # Initialize agent orchestrator
        orchestrator = AgentOrchestrator(
            user_id=current_user.id,
            domain=request.domain.value if request.domain else None,
            session_id=session_id
        )
        
        # Process message through agent system
        response_data = await orchestrator.process_message(request.message)
        
        execution_time = time.time() - start_time
        
        # Log activity
        activity_log = ActivityLog(
            user_id=current_user.id,
            action="chat_query",
            domain=request.domain.value if request.domain else None,
            query_text=request.message,
            response_summary=response_data.get("message", "")[:500],
            execution_time=execution_time,
            agent_interactions=response_data.get("agent_logs") if request.include_agent_logs else None
        )
        db.add(activity_log)
        await db.commit()
        
        logger.info(f"Chat processed for user {current_user.username} in {execution_time:.2f}s")
        
        return ChatResponse(
            message=response_data["message"],
            session_id=session_id,
            domain=request.domain,
            agent_logs=response_data.get("agent_logs") if request.include_agent_logs else None,
            visualization=response_data.get("visualization"),
            sql_query=response_data.get("sql_query"),
            data=response_data.get("data"),
            execution_time=execution_time
        )
        
    except Exception as e:
        logger.error(f"Chat error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")


@router.get("/history/{session_id}")
async def get_chat_history(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get chat history for a session"""
    
    from sqlalchemy import select
    
    result = await db.execute(
        select(Conversation).filter(
            Conversation.session_id == session_id,
            Conversation.user_id == current_user.id
        )
    )
    conversation = result.scalar_one_or_none()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return {
        "session_id": session_id,
        "messages": conversation.messages,
        "domain": conversation.domain,
        "created_at": conversation.created_at
    }


@router.delete("/history/{session_id}")
async def delete_chat_history(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete chat history"""
    
    from sqlalchemy import select, delete
    
    result = await db.execute(
        select(Conversation).filter(
            Conversation.session_id == session_id,
            Conversation.user_id == current_user.id
        )
    )
    conversation = result.scalar_one_or_none()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    await db.execute(
        delete(Conversation).filter(Conversation.session_id == session_id)
    )
    await db.commit()
    
    return {"message": "Chat history deleted successfully"}
