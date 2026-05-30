import onnxruntime as ort
import numpy as np
from PIL import Image
import io
import os
from pathlib import Path

session = ort.InferenceSession('best.onnx')

def is_pothole(image_bytes: bytes) -> bool:
    image = Image.open(io.BytesIO(image_bytes)).resize((224, 224))
    img_array = np.array(image).astype(np.float32) / 255.0
    
    # Apply same normalization as training ← add this
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    img_array = (img_array - mean) / std
    
    img_array = img_array.transpose(2, 0, 1)
    img_array = np.expand_dims(img_array, 0).astype(np.float32)

    outputs = session.run(None, {'images': img_array})
    predicted_class = np.argmax(outputs[0])
    
    return predicted_class == 1

if __name__ == "__main__":
    # Simple test using testphoto.jpg
    test_image_path = Path("testphoto.jpg")  # needs `from pathlib import Path`

    if not os.path.exists(test_image_path):
        raise FileNotFoundError(f"Test image not found: {test_image_path}")
    with open(test_image_path, "rb") as f:
        img_bytes = f.read()
    result = is_pothole(img_bytes)
    print(f"Pothole detection result for {test_image_path.name}: {result}")