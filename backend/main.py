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

def is_duplicate_location(location: str, radius_metres: int = 10) -> bool:
    """Returns True if a pothole already exists within radius_metres of the given location."""
    if not location:
        return False
    try:
        coords = location.replace("POINT(", "").replace(")", "").split()
        lng, lat = float(coords[0]), float(coords[1])
        result = supabase.rpc("is_duplicate_pothole", {"lat": lat, "lng": lng}).execute()
        return bool(result.data)
    except Exception as e:
        print(f"Duplicate check failed: {e}")
        return False  # Fail open — don't block upload if check errors



    
async def upload_to_supabase(image_bytes: bytes, filename: str, image_upload: ImageUpload) -> dict:
    """Uploads image to Supabase storage and inserts record into DB. Returns result dict."""
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

    try:
        data = image_upload.to_db_record(public_url)
        response = supabase.table("potholes").insert(data).execute()
        return {"message": "Pothole uploaded!", "data": response.data, "image_url": public_url}
    except Exception as e:
        return {"error": f"DB insert failed: {str(e)}"}


@app.post("/master_upload")
async def master_upload(
    file: UploadFile = File(None),
    location: str = Form(None),
    status: str = Form(None),
    file_path: str = Form(None),
):
    image_upload = ImageUpload(
        created_at=datetime.utcnow().isoformat(),
        image_url="",
        location=location,
        status=status,
        file_path=file_path
    )

    if file:
        image_bytes = await file.read()
        filename = file.filename
    else:
        image_bytes = image_upload.get_image_bytes()
        filename = image_upload.get_filename()

    if not is_pothole(image_bytes):
        return {"message": "The image does not contain a pothole."}

    if is_duplicate_location(location):
        return {"message": "A pothole has already been reported within 10 metres of this location."}

    return await upload_to_supabase(image_bytes, filename, image_upload)


import struct

def wkb_to_wkt(wkb_hex: str) -> str:
    if not wkb_hex:
        return ""
    if wkb_hex.startswith("POINT"):
        return wkb_hex
    try:
        wkb_bytes = bytes.fromhex(wkb_hex)
        byte_order = wkb_bytes[0]
        fmt = '<' if byte_order == 1 else '>'
        
        geom_type = struct.unpack(fmt + 'I', wkb_bytes[1:5])[0]
        has_srid = bool(geom_type & 0x20000000)
        
        offset = 5
        if has_srid:
            offset = 9
            
        x, y = struct.unpack(fmt + 'dd', wkb_bytes[offset:offset+16])
        return f"POINT({x} {y})"
    except Exception as e:
        print(f"Error parsing WKB: {e}")
        return wkb_hex

@app.get("/potholes")
async def get_potholes():
    response = supabase.table("potholes").select("*").execute()
    data = response.data or []
    for record in data:
        if "location" in record and record["location"]:
            record["location"] = wkb_to_wkt(record["location"])
    return data

    



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



