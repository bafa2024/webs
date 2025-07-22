from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Any
from uuid import UUID
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]

class UserCreate(UserBase):
    password: str
    confirm_password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(UserBase):
    id: UUID
    is_active: bool
    is_verified: bool
    subscription_plan: str
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        orm_mode = True

# Auth responses
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserOut

# Job schemas
class JobBase(BaseModel):
    name: str
    settings: Optional[Any]
    output_directory: str

class JobCreate(JobBase):
    pages: List[Any]  # List of dicts with url, save_path

class JobOut(JobBase):
    id: UUID
    status: str
    created_at: datetime
    updated_at: datetime
    total_pages: Optional[int]
    completed_pages: Optional[int]
    failed_pages: Optional[int]

    class Config:
        orm_mode = True

# Page schemas
class PageBase(BaseModel):
    url: str
    save_path: str

class PageOut(PageBase):
    id: UUID
    status: str
    created_at: datetime
    completed_at: Optional[datetime]
    error_message: Optional[str]
    file_size: Optional[int]
    asset_count: Optional[int]

    class Config:
        orm_mode = True

# Asset schemas
class AssetBase(BaseModel):
    url: str
    local_path: str
    asset_type: str

class AssetOut(AssetBase):
    id: UUID
    file_size: Optional[int]
    downloaded_at: datetime

    class Config:
        orm_mode = True 