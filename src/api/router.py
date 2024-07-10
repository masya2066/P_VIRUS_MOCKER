from fastapi import APIRouter, Depends, Form, File, Path, UploadFile, BackgroundTasks
from src.api.handlers.kata import create_kata, get_scans, delete_scan
from sqlalchemy.orm import Session
from src.database.database import get_db
router = APIRouter()


@router.post("/kata/scanner/v1", tags=["kata"])
async def CreateKata(
    db: Session = Depends(get_db),
    objectType: str = Form(...),
    scanId: str = Form(...),
    content: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    file = await content.read()
    return create_kata(db, objectType, scanId, file, background_tasks)


@router.get("/kata/scanner/v1/state", tags=["kata"])
async def GetScans(db: Session = Depends(get_db)):
    return get_scans(db)


@router.delete("/kata/scanner/v1/{scan_id}", tags=["kata"])
async def DeleteKata(db: Session = Depends(get_db), scan_id: str = Path(..., description="The scan ID to delete")):
    return delete_scan(db, scan_id)
