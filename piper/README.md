# Text to Speech Converter

A Flask web application that converts text to speech using Piper TTS.

## Features

- Convert text to speech in real-time
- Upload and extract text from common file formats (TXT, PDF, DOCX, RTF)
- Drag and drop file upload support
- Play audio directly in the browser
- Download generated audio files
- Modern, responsive UI

## Supported File Formats

- **TXT**: Plain text files
- **PDF**: Portable Document Format files
- **DOCX**: Microsoft Word documents
- **RTF**: Rich Text Format files

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
http://localhost:8888
```

## Usage

### Method 1: Direct Text Input
1. Enter or paste the text you want to convert to speech in the text area
2. Click "Convert to Speech"
3. Wait for the conversion to complete
4. Use the audio player to listen to the generated speech
5. Click "Download Audio" to save the audio file

### Method 2: File Upload
1. Click on the upload area or drag and drop a supported file
2. The text will be automatically extracted and populated in the text area
3. Review and edit the extracted text if needed
4. Click "Convert to Speech"
5. Wait for the conversion to complete
6. Use the audio player to listen to the generated speech
7. Click "Download Audio" to save the audio file

## File Upload Limitations

- Maximum file size: 10MB
- Supported formats: TXT, PDF, DOCX, RTF
- Files are processed temporarily and not stored on the server

## License

MIT License
