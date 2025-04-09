from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tensorflow as tf
from PIL import Image
import numpy as np
import io
import os

app = FastAPI()

# Enable CORS with specific settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the absolute path to the model file
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'pothole_classifier_final.keras')

# Load the model
model = tf.keras.models.load_model(model_path)

def preprocess_image(image):
    # Resize image to match model's expected sizing (150x150)
    image = image.resize((150, 150))
    # Convert to numpy array
    image_array = np.array(image)
    # Normalize the image (same as in training: rescale=1./255)
    image_array = image_array / 255.0
    # Add batch dimension
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

@app.post("/predict")
async def predict_pothole(file: UploadFile = File(...)):
    try:
        # Read the uploaded file
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Preprocess the image
        processed_image = preprocess_image(image)
        
        # Make prediction
        prediction = model.predict(processed_image)
        
        # Get the probability of pothole
        pothole_probability = float(prediction[0][0])
        
        # Use a higher threshold (0.7) for more confident predictions
        # Also consider the inverse probability for "no pothole" confidence
        is_pothole = pothole_probability > 0.7
        confidence = pothole_probability if is_pothole else (1 - pothole_probability)
        
        return JSONResponse({
            "is_pothole": bool(is_pothole),
            "confidence": float(confidence),
            "raw_probability": float(pothole_probability)
        })
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@app.get("/")
async def root():
    return {"message": "Pothole Detection System API"} 