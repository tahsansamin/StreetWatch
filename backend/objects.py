# from datetime import datetime
from pydantic import BaseModel
from typing import Optional
import os

class ImageUpload(BaseModel):
    created_at: str  # datetime or str
    image_url: str    # str
    location: str     # str
    status: str       # str
    file_path: Optional[str] = None  # str

    def get_image_bytes(self) -> bytes:
        if self.file_path:
            with open(self.file_path, "rb") as f:
                return f.read()
        raise ValueError("No file path provided.")

    def get_filename(self) -> str:
        if self.file_path:
            return os.path.basename(self.file_path)
        raise ValueError("No file path provided.")
    def to_db_record(self, image_url: str) -> dict:
        return {
            "created_at": self.created_at or datetime.utcnow().isoformat(),
            "image_url": image_url,
            "location": self.location,
            "status": self.status,
        }


