from google import genai
from PIL import Image
from dotenv import load_dotenv
import os
import json
import re



from google import genai
from PIL import Image
from dotenv import load_dotenv
import os
import json
import re
import io

load_dotenv()

def is_pothole(image_source: bytes | str) -> bool:
    # Accept either bytes or a file path string
    if isinstance(image_source, bytes):
        image = Image.open(io.BytesIO(image_source))
    else:
        image = Image.open(image_source)

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            image,
            (
                "Return only a single JSON object with the key 'is_pothole' and a boolean value "
                "(true if the image is a pothole, false otherwise). "
                "Do not include any other text, explanation, or markdown formatting."
            )
        ]
    )

    clean = re.sub(r"```(?:json)?\s*|\s*```", "", response.text).strip()
    result = json.loads(clean)
    return result["is_pothole"]

