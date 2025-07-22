from fastapi import APIRouter, Depends, HTTPException, status
from uuid import uuid4, UUID
from datetime import datetime
from typing import Dict
from .schemas import PageBase, PageOut
from .auth import get_current_user

router = APIRouter()

# In-memory page store for demo
fake_pages_db: Dict[str, dict] = {}

@router.post("/scrape", response_model=PageOut)
def scrape_page(page: PageBase, current_user: dict = Depends(get_current_user)):
    page_id = uuid4()
    now = datetime.utcnow()
    # Simulate scraping logic
    page_dict = {
        "id": page_id,
        "url": page.url,
        "save_path": page.save_path,
        "status": "completed",
        "created_at": now,
        "completed_at": now,
        "error_message": None,
        "file_size": 12345,
        "asset_count": 3,
    }
    fake_pages_db[str(page_id)] = page_dict
    return PageOut(**page_dict)

@router.get("/{page_id}", response_model=PageOut)
def get_page(page_id: UUID, current_user: dict = Depends(get_current_user)):
    page = fake_pages_db.get(str(page_id))
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return PageOut(**page) 