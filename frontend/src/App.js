import React, { useState } from 'react';
import { 
  Container, 
  Box, 
  Typography, 
  Paper, 
  CircularProgress,
  Alert,
  ThemeProvider,
  createTheme
} from '@mui/material';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

// Create axios instance with base URL
const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000, // 10 seconds timeout
});

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const onDrop = (acceptedFiles) => {
    setFile(acceptedFiles[0]);
    setResult(null);
    setError(null);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png']
    },
    maxFiles: 1
  });

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await api.post('/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResult(response.data);
    } catch (err) {
      if (err.code === 'ECONNABORTED') {
        setError('Request timed out. Please try again.');
      } else if (err.response) {
        setError(`Server error: ${err.response.data.error || 'Unknown error'}`);
      } else if (err.request) {
        setError('Could not connect to the server. Please make sure the backend is running.');
      } else {
        setError('An error occurred. Please try again.');
      }
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <Container maxWidth="md">
        <Box sx={{ my: 4 }}>
          <Typography variant="h3" component="h1" gutterBottom align="center" color="primary">
            Pothole Detection System
          </Typography>
          
          <Paper
            {...getRootProps()}
            sx={{
              p: 4,
              mt: 4,
              textAlign: 'center',
              cursor: 'pointer',
              backgroundColor: isDragActive ? 'rgba(25, 118, 210, 0.08)' : 'background.paper',
              border: '2px dashed',
              borderColor: isDragActive ? 'primary.main' : 'grey.300',
            }}
          >
            <input {...getInputProps()} />
            <CloudUploadIcon sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
            <Typography variant="h6" gutterBottom>
              {isDragActive
                ? "Drop the image here"
                : "Drag and drop an image here, or click to select"}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Supported formats: JPEG, JPG, PNG
            </Typography>
          </Paper>

          {file && (
            <Box sx={{ mt: 2, textAlign: 'center' }}>
              <Typography variant="subtitle1">
                Selected file: {file.name}
              </Typography>
              <img
                src={URL.createObjectURL(file)}
                alt="Preview"
                style={{ maxWidth: '100%', maxHeight: '300px', marginTop: '16px' }}
              />
            </Box>
          )}

          {file && !loading && !result && (
            <Box sx={{ mt: 2, textAlign: 'center' }}>
              <button
                onClick={handleUpload}
                style={{
                  padding: '10px 20px',
                  fontSize: '16px',
                  backgroundColor: '#1976d2',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer',
                }}
              >
                Analyze Image
              </button>
            </Box>
          )}

          {loading && (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
              <CircularProgress />
            </Box>
          )}

          {error && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {error}
            </Alert>
          )}

          {result && (
            <Paper sx={{ p: 3, mt: 4, textAlign: 'center' }}>
              <Typography variant="h5" gutterBottom>
                Analysis Result
              </Typography>
              <Typography variant="h6" color={result.is_pothole ? 'error' : 'success.main'}>
                {result.is_pothole ? 'Pothole Detected!' : 'No Pothole Detected'}
              </Typography>
              <Typography variant="body1" sx={{ mt: 2 }}>
                Confidence: {(result.confidence * 100).toFixed(2)}%
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                Raw Probability: {(result.raw_probability * 100).toFixed(2)}%
              </Typography>
              {result.raw_probability > 0.3 && result.raw_probability < 0.7 && (
                <Alert severity="warning" sx={{ mt: 2 }}>
                  Low confidence prediction. Please verify manually.
                </Alert>
              )}
            </Paper>
          )}
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App; 