# Text to Speech API

A FastAPI-based application that provides text-to-speech functionality using the OpenAI API.

## Prerequisites

- Python 3.12 or higher
- UV package manager

## Setup

1. Install UV if you haven't already:
```bash
pip install uv
```

2. Create a virtual environment and install dependencies:
```bash
uv venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
uv pip install -r requirements.txt
```

3. Create a `.env` file in the project root:
```bash
# Copy the example .env file
cp .env.example .env
```

4. Edit the `.env` file and set your environment variables:
```env
OPENAI_API_KEY=your-api-key-here
OPENAI_BASE_URL=your-custom-base-url  # Optional, defaults to https://api.openai.com/v1
```

## Running the Application

Start the server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### GET /
Health check endpoint that returns a simple message.

### POST /text-to-speech
Converts text to speech.

Request body:
```json
{
    "text": "Text to convert to speech",
    "voice": "alloy",  // Optional, defaults to "alloy"
    "model": "tts-1"   // Optional, defaults to "tts-1"
}
```

Response: Audio file in MP3 format

## Available Voices
- alloy
- echo
- fable
- onyx
- nova
- shimmer

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc` 