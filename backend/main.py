
from fastapi import FastAPI
from objects import ImageUpload
from supabase import create_client, Client
import os
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
import mimetypes
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
    data = {
        "created_at": image_upload.created_at,
        "image_url": image_upload.image_url,
        "location": image_upload.location,
        "status": image_upload.status
    }
    ext = os.path.splitext(image_upload.file_path)[1].lower()
    content_type = CONTENT_TYPE_MAP.get(ext, "application/octet-stream")
    try :
        with open(image_upload.file_path, "rb") as f:
            res = supabase.storage.from_("pothole_images").upload(
            path="pothole.jpg",
            file=f, 
            file_options={
             "content-type": content_type
            }
        
    )   
        return {"message": "Image uploaded to Supabase Storage", "response": res}
    except Exception as e:
        return {"error": str(e)}
    try:
        response = supabase.table("potholes").insert(data).execute()
        return {"message": "Image uploaded to Supabase", "data": response.data}
    except Exception as e:
        return {"error": str(e)}
    

   
    
