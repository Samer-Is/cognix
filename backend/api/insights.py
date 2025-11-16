"""
Insights API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from datetime import datetime

from database.connection import get_db
from database.models import User
from database.schemas import InsightRequest, InsightResponse, Insight
from api.auth import get_current_user
from services.analytics_service import AnalyticsService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("", response_model=InsightResponse)
async def get_insights(
    request: InsightRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get automated insights for a domain"""
    
    try:
        analytics_service = AnalyticsService(
            domain=request.domain.value,
            user_id=current_user.id
        )
        
        insights = await analytics_service.generate_insights(
            timeframe=request.timeframe,
            insight_types=request.insight_types
        )
        
        logger.info(f"Generated {len(insights)} insights for {request.domain.value}")
        
        return InsightResponse(
            insights=insights,
            domain=request.domain
        )
        
    except Exception as e:
        logger.error(f"Error generating insights: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error generating insights: {str(e)}")


@router.get("/proactive")
async def get_proactive_insights(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get proactive insights across all domains"""
    
    # This would run periodic checks and generate alerts
    # For now, returning placeholder
    
    return {
        "insights": [],
        "message": "Proactive insights will be generated periodically"
    }
