from asyncio import sleep
from datetime import datetime
from typing import Any, Coroutine

from fastapi import HTTPException
from src.models.kataFile import KataFile
from src.consumer.kata_consumer import check_file
from typing import List, Dict
from src.utils.models import model_to_dict


async def kata_bg_checker(db, file: Coroutine[Any, Any, bytes], scan_id: str, timeout: int):
    if timeout < 5:
        timeout = 5
    await sleep(timeout)
    await check_file(db, file=file, scan_id=scan_id)


def kata_transform_data(data: List[Dict[str, any]]) -> List[Dict[str, any]]:
    filtered_data = [
        {
            "scan_id": item["scan_id"],
            "state": item["state"]
        }
        for item in data

    ]
    return filtered_data


def create_kata(db, object_type: str, scan_id: str, content: Coroutine[Any, Any, bytes], background_tasks):
    existing_kata = db.query(KataFile).filter(
        KataFile.scan_id == scan_id).first()

    if object_type != "file":
        raise HTTPException(status_code=400, detail={
                            "message": f"Object type '{object_type}' not supported."})

    if existing_kata:
        existing_kata.state = "processing"
        existing_kata.updated_at = datetime.now()
        db.commit()
        db.refresh(existing_kata)
        raise HTTPException(status_code=400, detail={
                            "message": f"Record with scan_id '{scan_id}' already exists."})
    else:
        file_size_mb = content.__sizeof__() / (1024 * 1024)
        timeout = file_size_mb * 4

        db_kata = KataFile(
            scan_id=scan_id,
            state="processing",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        db.add(db_kata)
        db.commit()
        db.refresh(db_kata)
        print(f"Record with scan_id '{scan_id}' created.")

        background_tasks.add_task(
            kata_bg_checker, db, content, scan_id, timeout)

        return {"status": "OK", "scan_id": scan_id}


def get_scans(db):
    # Fetch data from the database
    res = db.query(KataFile).all()
    # Convert each ORM instance to a dictionary
    dict_data = [model_to_dict(item) for item in res]
    # Transform the data
    return kata_transform_data(dict_data)


def delete_scan(db, scan_id: str):
    try:
        record = db.query(KataFile).filter(
            KataFile.scan_id == scan_id).one_or_none()

        if record is None:
            raise HTTPException(status_code=404, detail="Record not found")

        db.delete(record)
        db.commit()

        return {"OK"}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred")
