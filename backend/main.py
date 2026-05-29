import uuid
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, Form, UploadFile
from objects import ImageUpload
from supabase import create_client, Client
import os
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
import mimetypes
from pathlib import Path
from detecting_pothole import is_pothole
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


# verifies that what is being uploaded is a pothole, returns true if it is, false otherwise
@app.get("/verify_pothole")
async def get_potholes(image_upload: ImageUpload):
    return is_pothole(image_upload.file_path)


# # uploads the image to supabase storage and then inserts a record into the potholes table with the image URL and other metadata
# @app.post("/upload_image_to_supabase")
# async def upload_image(image_upload: ImageUpload):
#     # Example test object to upload
#     ext = os.path.splitext(image_upload.file_path)[1].lower()
#     content_type = CONTENT_TYPE_MAP.get(ext, "application/octet-stream")
#     file_name = Path(image_upload.file_path).name
#     bucket_folder = "19veqq_0"
#     storage_path = f"{bucket_folder}/{file_name}"
#     try:
#         with open(image_upload.file_path, "rb") as f:
#             res = supabase.storage.from_("pothole_images").upload(
#                 path=storage_path,
#                 file=f,
#                 file_options={
#                     "cache-control": "3600",
#                     "content-type": content_type,
#                     "upsert": "true"
#                 }
#             )
#         # Construct the public URL for the uploaded image
#         public_url = supabase.storage.from_("pothole_images").get_public_url(storage_path)
#     except Exception as e:
#         return {"error": f"Storage upload failed: {str(e)}"}

#     # Prepare data for DB insert
#     data = {
#         "created_at": image_upload.created_at or datetime.utcnow().isoformat(),
#         "image_url": public_url,
#         "location": image_upload.location,
#         "status": image_upload.status
#     }
#     try:
#         response = supabase.table("potholes").insert(data).execute()
#         return {"message": "Image uploaded to Supabase", "data": response.data, "image_url": public_url}
#     except Exception as e:
#         return {"error": f"DB insert failed: {str(e)}"}
    
@app.post("/master_upload")
async def master_upload(file: UploadFile = File(None),
    location: str = Form(None),
    status: str = Form(None),
    file_path: str = Form(None),
    ):
    image_upload = ImageUpload(
        created_at=datetime.utcnow().isoformat(),
        image_url="",  # This will be set after uploading to Supabase
        location=location,
        status=status,
        file_path=file_path
    )

    # Get bytes from either the uploaded file or the file path
    if file:
        image_bytes = await file.read()
        filename = file.filename
    else:
        image_bytes = image_upload.get_image_bytes()
        filename = image_upload.get_filename()
    if not is_pothole(image_bytes):
        return {"message": "The image does not contain a pothole."}
    
    # Upload to Supabase
    ext = os.path.splitext(filename)[1].lower()
    content_type = CONTENT_TYPE_MAP.get(ext, "image/jpeg")
    storage_path = f"19veqq_0/{uuid.uuid4()}{ext}"
    
    try:
        supabase.storage.from_("pothole_images").upload(
            path=storage_path,
            file=image_bytes,
            file_options={
                "cache-control": "3600",
                "content-type": content_type,
                "upsert": "true"
            }
        )
        public_url = supabase.storage.from_("pothole_images").get_public_url(storage_path)
    except Exception as e:
        return {"error": f"Storage upload failed: {str(e)}"}
    data = image_upload.to_db_record(public_url)
    try:
        response = supabase.table("potholes").insert(data).execute()
        return {"message": "Pothole uploaded!", "data": response.data, "image_url": public_url}
    except Exception as e:
        return {"error": f"DB insert failed: {str(e)}"}

    



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



