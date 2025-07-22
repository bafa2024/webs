from sqlalchemy import Column, String, Integer, Boolean, DateTime, Enum, ForeignKey, Text, JSON, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from .database import Base
import enum
from datetime import datetime

class SubscriptionPlan(str, enum.Enum):
    free = "free"
    pro = "pro"
    enterprise = "enterprise"

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    subscription_plan = Column(Enum(SubscriptionPlan), default=SubscriptionPlan.free)
    sessions = relationship("UserSession", back_populates="user")
    jobs = relationship("Job", back_populates="user")

class UserSession(Base):
    __tablename__ = "user_sessions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    refresh_token = Column(String(512), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(64))
    user_agent = Column(Text)
    user = relationship("User", back_populates="sessions")

class JobStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"
    paused = "paused"

class Job(Base):
    __tablename__ = "jobs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    name = Column(String(255), nullable=False)
    status = Column(Enum(JobStatus), default=JobStatus.pending)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    total_pages = Column(Integer)
    completed_pages = Column(Integer, default=0)
    failed_pages = Column(Integer, default=0)
    settings = Column(JSON)
    output_directory = Column(Text, nullable=False)
    user = relationship("User", back_populates="jobs")
    pages = relationship("Page", back_populates="job")

class PageStatus(str, enum.Enum):
    pending = "pending"
    downloading = "downloading"
    completed = "completed"
    failed = "failed"

class Page(Base):
    __tablename__ = "pages"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id", ondelete="CASCADE"))
    url = Column(Text, nullable=False)
    save_path = Column(Text, nullable=False)
    status = Column(Enum(PageStatus), default=PageStatus.pending)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    error_message = Column(Text)
    file_size = Column(BigInteger)
    asset_count = Column(Integer, default=0)
    job = relationship("Job", back_populates="pages")
    assets = relationship("Asset", back_populates="page")

class AssetType(str, enum.Enum):
    css = "css"
    js = "js"
    image = "image"
    font = "font"
    other = "other"

class Asset(Base):
    __tablename__ = "assets"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    page_id = Column(UUID(as_uuid=True), ForeignKey("pages.id", ondelete="CASCADE"))
    url = Column(Text, nullable=False)
    local_path = Column(Text, nullable=False)
    asset_type = Column(Enum(AssetType))
    file_size = Column(BigInteger)
    downloaded_at = Column(DateTime, default=datetime.utcnow)
    page = relationship("Page", back_populates="assets") 