import datetime

from fastapi import UploadFile
from src.models.kataFile import KataFile
from src.utils.files import check_text_in_file
from sqlalchemy.orm import Session


async def check_file(db: Session, file: any, scan_id: str):

    now = datetime.datetime.now()
    is_exist = await check_text_in_file(file, "virus_exist")
    state = "detect" if is_exist else "not detect"

    try:
        rows_updated = db.query(KataFile).filter(KataFile.scan_id == scan_id).update(
            {"state": state, "updated_at": now}
        )

        if rows_updated:
            print("ScanId: ", scan_id, "updated successfully. State: ", state)

        db.commit()

    except Exception as e:
        print(f"An error occurred during the update: {e}")
        db.rollback()
