# Text to Speech Converter

A Flask web application that converts text to speech using Piper TTS.

## Features

- Convert text to speech in real-time
- Play audio directly in the browser
- Download generated audio files
- Modern, responsive UI

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download Piper TTS model:
You need to download the Piper TTS model files. For this example, we're using the English (US) Lessac Medium model. Place the following files in the project root:
- `en_US-lessac-medium.onnx`
- `en_US-lessac-medium.onnx.json`

You can download these files from the [Piper TTS releases page](https://github.com/rhasspy/piper/releases).

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage

1. Enter or paste the text you want to convert to speech
2. Click "Convert to Speech"
3. Wait for the conversion to complete
4. Use the audio player to listen to the generated speech
5. Click "Download Audio" to save the audio file

## License

MIT License
