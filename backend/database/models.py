"""
Database models for COGNIX AI
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.connection import Base


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    role = Column(String(50), default="analyst")  # admin, analyst, viewer
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    activity_logs = relationship("ActivityLog", back_populates="user")
    saved_queries = relationship("SavedQuery", back_populates="user")


class ActivityLog(Base):
    """Activity logging model"""
    __tablename__ = "activity_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(100), nullable=False)  # query, domain_switch, upload, etc.
    domain = Column(String(50))
    query_text = Column(Text)
    response_summary = Column(Text)
    execution_time = Column(Float)  # seconds
    agent_interactions = Column(JSON)  # Agent conversation logs
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="activity_logs")


class SavedQuery(Base):
    """Saved queries model"""
    __tablename__ = "saved_queries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    domain = Column(String(50), nullable=False)
    query_text = Column(Text, nullable=False)
    sql_query = Column(Text)
    visualization_config = Column(JSON)
    is_favorite = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="saved_queries")


class Alert(Base):
    """Alerts and notifications model"""
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    domain = Column(String(50), nullable=False)
    alert_type = Column(String(50), nullable=False)  # anomaly, threshold, insight
    title = Column(String(255), nullable=False)
    description = Column(Text)
    severity = Column(String(20), default="info")  # info, warning, critical
    metric_name = Column(String(100))
    metric_value = Column(Float)
    threshold_value = Column(Float)
    condition = Column(JSON)
    is_read = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User")


class Conversation(Base):
    """Conversation history model"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(String(100), unique=True, index=True, nullable=False)
    domain = Column(String(50))
    messages = Column(JSON, nullable=False)  # Array of message objects
    agent_logs = Column(JSON)  # Agent interaction logs
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User")


class UploadedFile(Base):
    """Uploaded files for RAG model"""
    __tablename__ = "uploaded_files"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)  # pdf, docx, csv
    file_size = Column(Integer)  # bytes
    s3_key = Column(String(500), nullable=False)
    status = Column(String(50), default="processing")  # processing, ready, failed
    num_chunks = Column(Integer)
    embedding_status = Column(String(50))
    metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User")
