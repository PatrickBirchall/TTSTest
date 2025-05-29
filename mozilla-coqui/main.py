from flask import Flask, render_template, request, send_file, jsonify
from TTS.api import TTS
import os
import uuid

app = Flask(__name__)

# Initialize TTS
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)

# Ensure audio_files directory exists
AUDIO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audio_files')
os.makedirs(AUDIO_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/synthesize', methods=['POST'])
def synthesize():
    try:
        text = request.json.get('text', '')
        if not text:
            return jsonify({'error': 'No text provided'}), 400

        # Create a unique filename in our audio_files directory
        output_file = os.path.join(AUDIO_DIR, f"{uuid.uuid4()}.wav")
        
        # Generate speech
        tts.tts_to_file(text=text, file_path=output_file, model_name="tts_models/en/jenny/jenny")
        
        # Return the relative path for the frontend to use
        relative_path = os.path.relpath(output_file, os.path.dirname(os.path.abspath(__file__)))
        return jsonify({
            'success': True,
            'file_path': relative_path
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/audio/<path:filename>')
def serve_audio(filename):
    return send_file(filename, mimetype='audio/wav')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8888)
