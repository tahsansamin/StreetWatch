# from datetime import datetime
from pydantic import BaseModel

class ImageUpload(BaseModel):
	created_at: str  # datetime or str
	image_url: str    # str
	location: str     # str
	status: str       # str
	file_path: str       # str


