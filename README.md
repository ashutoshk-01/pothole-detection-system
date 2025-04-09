# Pothole Detection System

A full-stack application for detecting potholes in images using machine learning. This project combines a TensorFlow-based CNN model with a FastAPI backend and React frontend to provide a user-friendly interface for pothole detection.

## Features

- Upload images through a modern, responsive UI
- Real-time pothole detection using a trained CNN model
- Confidence scoring for predictions
- Detailed analysis results with visual feedback

## Project Structure

```
.
├── backend/           # FastAPI backend
│   └── main.py       # Backend server code
├── frontend/         # React frontend
│   ├── src/
│   │   └── App.js    # Frontend application
│   └── package.json  # Frontend dependencies
├── requirements.txt  # Python dependencies
└── README.md        # This file
```

## Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

## Setup Instructions

### Backend Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Run the backend server:
```bash
cd backend
python -m uvicorn main:app --reload
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Install Node.js dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Drag and drop an image or click to select one
3. Click "Analyze Image" to process the image
4. View the results showing whether a pothole was detected and the confidence level

## API Endpoints

- `POST /predict`: Upload an image for pothole detection
  - Returns: JSON with `is_pothole` (boolean), `confidence` (float), and `raw_probability` (float) fields

## Model Architecture

The model uses a CNN architecture with:
- Input size: 150x150 pixels
- Three convolutional layers with batch normalization
- Dropout layers for regularization
- Binary classification output

## Technologies Used

- Backend:
  - FastAPI
  - TensorFlow
  - Pillow

- Frontend:
  - React
  - Material-UI
  - React Dropzone
  - Axios

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to all contributors who have helped improve this project
- Special thanks to the open-source community for the amazing tools and libraries used in this project 