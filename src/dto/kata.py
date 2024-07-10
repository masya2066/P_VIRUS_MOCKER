from pydantic import BaseModel


class KataBase(BaseModel):
    id: int
    scan_id: str
    state: str
    created_at: str
    updated_at: str
