from flask import Flask, render_template, request, send_file, jsonify
import os
import tempfile
from piper import PiperVoice
import wave
import numpy as np
import io
import uuid

app = Flask(__name__)

# Create audio directory if it doesn't exist
AUDIO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audio_files')
os.makedirs(AUDIO_DIR, exist_ok=True)

# Initialize Piper TTS
model_path = "en_US-lessac-medium.onnx"
config_path = "en_US-lessac-medium.onnx.json"
voice = PiperVoice.load(model_path, config_path)

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

if __name__ == '__main__':
    app.run(debug=True, port=8888) 