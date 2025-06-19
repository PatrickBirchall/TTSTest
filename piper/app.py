from flask import Flask, render_template, request, send_file, jsonify
import os
import tempfile
from piper import PiperVoice
import wave
import numpy as np
import io
import uuid
import PyPDF2
from docx import Document
import striprtf.striprtf

app = Flask(__name__)

# Create audio directory if it doesn't exist
AUDIO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audio_files')
os.makedirs(AUDIO_DIR, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'rtf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_file(file_path, file_extension):
    """Extract text from various file formats"""
    try:
        if file_extension == 'txt':
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        
        elif file_extension == 'pdf':
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        
        elif file_extension == 'docx':
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        
        elif file_extension == 'rtf':
            with open(file_path, 'r', encoding='utf-8') as file:
                rtf_content = file.read()
                return striprtf.striprtf(rtf_content)
        
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    except Exception as e:
        raise Exception(f"Error extracting text from file: {str(e)}")

# Initialize Piper TTS
model_path = "en_US-lessac-high.onnx"
config_path = "en_US-lessac-high.onnx.json"
try:
    voice = PiperVoice.load(model_path, config_path)
except Exception as e:
    raise RuntimeError(f"Failed to load Piper voice model: {str(e)}. Have you downloaded the model files?")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_text():
    text = request.json.get('text', '')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        # Generate a unique filename
        filename = f"{uuid.uuid4()}.wav"
        file_path = os.path.join(AUDIO_DIR, filename)

        # Open the file as a WAV file
        with wave.open(file_path, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(22050)  # Sample rate
            # Generate speech directly to the WAV file
            voice.synthesize(text, wav_file)

        # Return the filename
        return jsonify({
            'audio_path': filename,
            'filename': 'speech.wav'
        })
    except Exception as e:
        # Clean up the file if it exists
        if 'file_path' in locals():
            try:
                os.unlink(file_path)
            except:
                pass
        return jsonify({'error': str(e)}), 500

@app.route('/audio/<path:filename>')
def serve_audio(filename):
    try:
        file_path = os.path.join(AUDIO_DIR, filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'Audio file not found'}), 404
            
        return send_file(
            file_path,
            mimetype='audio/wav',
            as_attachment=False,
            download_name='speech.wav'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not supported. Please upload .txt, .pdf, .docx, or .rtf files'}), 400
    
    try:
        # Save uploaded file temporarily
        temp_dir = tempfile.mkdtemp()
        temp_file_path = os.path.join(temp_dir, file.filename)
        file.save(temp_file_path)
        
        # Extract text from file
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        extracted_text = extract_text_from_file(temp_file_path, file_extension)
        
        # Clean up temporary file
        os.remove(temp_file_path)
        os.rmdir(temp_dir)
        
        if not extracted_text.strip():
            return jsonify({'error': 'No text could be extracted from the file'}), 400
        
        return jsonify({
            'text': extracted_text,
            'filename': file.filename
        })
    
    except Exception as e:
        # Clean up on error
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
                os.rmdir(temp_dir)
            except:
                pass
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8888) 