from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tensorflow as tf
from PIL import Image
import numpy as np
import io
import os
import logging

app = FastAPI()

# Enable CORS with specific settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Model configuration
IMG_HEIGHT = 150
IMG_WIDTH = 150
CLASS_THRESHOLD = 0.5  # Standard threshold for binary classification

# Get the absolute path to the model file
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'pothole_classifier.h5')

# Load the model
try:
    model = tf.keras.models.load_model(model_path)
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    raise

def preprocess_image(image):
    try:
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        # Resize image to match model's expected sizing
        image = image.resize((IMG_HEIGHT, IMG_WIDTH))
        
        # Convert to numpy array
        image_array = np.array(image)
        
        # Ensure the array has the correct shape
        if image_array.shape != (IMG_HEIGHT, IMG_WIDTH, 3):
            raise ValueError(f"Invalid image shape: {image_array.shape}")
            
        # Normalize the image (same as in training: rescale=1./255)
        image_array = image_array / 255.0
        
        # Add batch dimension
        image_array = np.expand_dims(image_array, axis=0)
        
        return image_array
    except Exception as e:
        logger.error(f"Error preprocessing image: {str(e)}")
        raise

@app.post("/predict")
async def predict_pothole(file: UploadFile = File(...)):
    try:
        # Read the uploaded file
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Log image details
        logger.info(f"Received image: {file.filename}, size: {image.size}, mode: {image.mode}")
        
        # Preprocess the image
        processed_image = preprocess_image(image)
        
        # Make prediction
        prediction = model.predict(processed_image, verbose=0)
        
        # Get the probability of pothole
        pothole_probability = float(prediction[0][0])
        
        # Log the raw prediction
        logger.info(f"Raw prediction probability: {pothole_probability}")
        
        # Use standard binary classification threshold
        is_pothole = pothole_probability > CLASS_THRESHOLD
        
        # Calculate confidence
        confidence = pothole_probability if is_pothole else (1 - pothole_probability)
            
        # Log the final decision
        logger.info(f"Final decision: {'Pothole' if is_pothole else 'Normal road'}, Confidence: {confidence:.2f}")
        
        return JSONResponse({
            "is_pothole": bool(is_pothole),
            "confidence": float(confidence),
            "raw_probability": float(pothole_probability)
        })
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@app.get("/")
async def root():
    return {"message": "Pothole Detection System API"} 