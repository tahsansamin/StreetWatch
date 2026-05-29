from google import genai
from PIL import Image
from dotenv import load_dotenv
import os
import json
import re



def is_pothole(image_path):
    load_dotenv()
    image = Image.open(image_path)

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

    # Strip markdown code fences if present
    clean = re.sub(r"```(?:json)?\s*|\s*```", "", response.text).strip()

    result = json.loads(clean)
    return result["is_pothole"]

if __name__ == "__main__":
    
    if is_pothole("MicrosoftTeams-image_32.jpg"):
        print("The image contains a pothole.")
    else:
        print("The image does not contain a pothole.")