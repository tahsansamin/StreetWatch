from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

image = Image.open("MicrosoftTeams-image_32.jpg")

response = client.models.generate_content(
    model="gemini-2.5-flash",  # ✅ fixed model name
    contents=[                  # ✅ contents must be a list
        image,
        "Describe what you see in this image."
    ]
)
    
print(response.text)
# or simply:
# print(response.text)