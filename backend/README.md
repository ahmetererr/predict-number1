# Digit Recognition Backend

This is the backend service for the Digit Recognition application. It provides API endpoints for digit prediction and model training.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the backend directory (optional):
```
MODEL_PATH=app/models/saved_model
```

## Running the Server

Start the development server:
```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `GET /` - Health check endpoint
- `POST /predict` - Predict a digit from an uploaded image
- `POST /train` - Train the model with a new image and its corresponding digit

## Project Structure

```
backend/
├── app/
│   ├── models/
│   │   ├── digit_recognizer.py
│   │   └── saved_model/
│   └── config.py
├── main.py
├── requirements.txt
└── README.md
``` 