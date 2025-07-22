from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from typing import List
import pandas as pd
from .auth import get_current_user

router = APIRouter()

@router.post("/spreadsheet")
def upload_spreadsheet(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    if not (file.filename.endswith('.csv') or file.filename.endswith('.xlsx')):
        raise HTTPException(status_code=400, detail="Only CSV or XLSX files are supported")
    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file.file)
        else:
            df = pd.read_excel(file.file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {e}")
    # Expect columns: url, save_path
    if not {'url', 'save_path'}.issubset(df.columns):
        raise HTTPException(status_code=400, detail="File must contain 'url' and 'save_path' columns")
    pages = df[['url', 'save_path']].to_dict(orient='records')
    return {"pages": pages, "count": len(pages)} 