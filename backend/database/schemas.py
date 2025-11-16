"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# ========== Enums ==========
class DomainType(str, Enum):
    TELECOM = "telecom"
    BANKING = "banking"
    DIGITAL_MARKETING = "digital_marketing"
    HEALTHCARE = "healthcare"
    FMCG = "fmcg"


class UserRole(str, Enum):
    ADMIN = "admin"
    ANALYST = "analyst"
    VIEWER = "viewer"


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


# ========== Auth Schemas ==========
class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str]
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ========== Chat Schemas ==========
class ChatMessage(BaseModel):
    role: MessageRole
    content: str
    timestamp: Optional[datetime] = None
    agent_name: Optional[str] = None


class ChatRequest(BaseModel):
    message: str
    domain: Optional[DomainType] = None
    session_id: Optional[str] = None
    include_agent_logs: bool = False


class AgentLog(BaseModel):
    agent_name: str
    action: str
    input: Dict[str, Any]
    output: Any
    timestamp: datetime
    execution_time: float


class ChatResponse(BaseModel):
    message: str
    session_id: str
    domain: Optional[DomainType]
    agent_logs: Optional[List[AgentLog]] = None
    visualization: Optional[Dict[str, Any]] = None
    sql_query: Optional[str] = None
    data: Optional[List[Dict[str, Any]]] = None
    execution_time: float


# ========== Domain Schemas ==========
class DomainInfo(BaseModel):
    name: DomainType
    display_name: str
    description: str
    tables: List[str]
    kpis: List[str]
    icon: str


class DomainListResponse(BaseModel):
    domains: List[DomainInfo]


class DomainSelectRequest(BaseModel):
    domain: DomainType


# ========== Query Schemas ==========
class QueryRequest(BaseModel):
    query: str
    domain: DomainType


class QueryResult(BaseModel):
    data: List[Dict[str, Any]]
    columns: List[str]
    row_count: int
    execution_time: float


# ========== Insight Schemas ==========
class InsightRequest(BaseModel):
    domain: DomainType
    timeframe: Optional[str] = "last_30_days"
    insight_types: Optional[List[str]] = ["trends", "anomalies", "predictions"]


class Insight(BaseModel):
    title: str
    description: str
    insight_type: str  # trend, anomaly, prediction, recommendation
    severity: str  # info, warning, critical
    metric_name: str
    current_value: Optional[float]
    previous_value: Optional[float]
    change_percentage: Optional[float]
    visualization: Optional[Dict[str, Any]]
    created_at: datetime


class InsightResponse(BaseModel):
    insights: List[Insight]
    domain: DomainType


# ========== File Upload Schemas ==========
class FileUploadResponse(BaseModel):
    file_id: int
    filename: str
    file_type: str
    file_size: int
    status: str
    message: str


class FileListResponse(BaseModel):
    files: List[Dict[str, Any]]


# ========== Saved Query Schemas ==========
class SavedQueryCreate(BaseModel):
    title: str
    description: Optional[str] = None
    domain: DomainType
    query_text: str
    sql_query: Optional[str] = None
    visualization_config: Optional[Dict[str, Any]] = None


class SavedQueryResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    domain: DomainType
    query_text: str
    is_favorite: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ========== Activity Log Schemas ==========
class ActivityLogResponse(BaseModel):
    id: int
    action: str
    domain: Optional[str]
    query_text: Optional[str]
    execution_time: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True
