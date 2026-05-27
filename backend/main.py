from fastapi import FastAPI
from objects import ImageUpload
from supabase import create_client, Client
import os
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
import mimetypes
from pathlib import Path
load_dotenv()
dotenvpath = find_dotenv()



CONTENT_TYPE_MAP = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".gif": "image/gif",
}

# Set your Supabase URL and Key here (replace with your actual credentials)
SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY")
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL and Key must be set in environment variables.")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/upload_image")
async def upload_image(image_upload: ImageUpload):
    # Example test object to upload
    ext = os.path.splitext(image_upload.file_path)[1].lower()
    content_type = CONTENT_TYPE_MAP.get(ext, "application/octet-stream")
    file_name = Path(image_upload.file_path).name
    bucket_folder = "19veqq_0"
    storage_path = f"{bucket_folder}/{file_name}"
    try:
        with open(image_upload.file_path, "rb") as f:
            res = supabase.storage.from_("pothole_images").upload(
                path=storage_path,
                file=f,
                file_options={
                    "cache-control": "3600",
                    "content-type": content_type,
                    "upsert": "true"
                }
            )
        # Construct the public URL for the uploaded image
        public_url = supabase.storage.from_("pothole_images").get_public_url(storage_path)
    except Exception as e:
        return {"error": f"Storage upload failed: {str(e)}"}

    # Prepare data for DB insert
    data = {
        "created_at": image_upload.created_at or datetime.utcnow().isoformat(),
        "image_url": public_url,
        "location": image_upload.location,
        "status": image_upload.status
    }
    try:
        response = supabase.table("potholes").insert(data).execute()
        return {"message": "Image uploaded to Supabase", "data": response.data, "image_url": public_url}
    except Exception as e:
        return {"error": f"DB insert failed: {str(e)}"}




