document.addEventListener('DOMContentLoaded', () => {
    const ttsForm = document.getElementById('ttsForm');
    const documentForm = document.getElementById('documentForm');
    const audioContainer = document.getElementById('audioContainer');
    const audioPlayer = document.getElementById('audioPlayer');
    const downloadBtn = document.getElementById('downloadBtn');
    const errorDiv = document.getElementById('error');

    // Function to handle audio response
    const handleAudioResponse = async (response) => {
        if (!response.ok) {
            throw new Error('Failed to generate speech');
        }

        const blob = await response.blob();
        const audioUrl = URL.createObjectURL(blob);
        
        audioPlayer.src = audioUrl;
        audioContainer.style.display = 'block';
        
        // Set up download button
        downloadBtn.onclick = () => {
            const a = document.createElement('a');
            a.href = audioUrl;
            a.download = 'speech.mp3';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        };
    };

    // Handle text-to-speech form submission
    ttsForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = {
            text: document.getElementById('text').value,
            voice: document.getElementById('voice').value,
            model: 'tts-1'
        };

        try {
            errorDiv.style.display = 'none';
            const response = await fetch('/text-to-speech', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            await handleAudioResponse(response);
        } catch (error) {
            errorDiv.textContent = error.message;
            errorDiv.style.display = 'block';
            audioContainer.style.display = 'none';
        }
    });

    // Handle document-to-speech form submission
    documentForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const fileInput = document.getElementById('document');
        const file = fileInput.files[0];
        
        if (!file) {
            errorDiv.textContent = 'Please select a file';
            errorDiv.style.display = 'block';
            return;
        }

        const formData = new FormData();
        formData.append('file', file);
        formData.append('voice', document.getElementById('docVoice').value);
        formData.append('model', 'tts-1');

        try {
            errorDiv.style.display = 'none';
            const response = await fetch('/document-to-speech', {
                method: 'POST',
                body: formData
            });

            await handleAudioResponse(response);
        } catch (error) {
            errorDiv.textContent = error.message;
            errorDiv.style.display = 'block';
            audioContainer.style.display = 'none';
        }
    });
}); 