"""
Model downloader for Piper TTS models from Hugging Face.

This module provides functionality to download Piper TTS model files
from the Hugging Face repository.
"""

import urllib.request
import urllib.error
from pathlib import Path


def download_models(model_name="en_GB-alan-medium", version="v1.0.0", download_dir="."):
    """
    Download Piper TTS model files from Hugging Face.
    
    Args:
        model_name (str): Name of the model (e.g., "en_GB-alan-medium")
        version (str): Version of the model (e.g., "v1.0.0")
        download_dir (str): Directory to download files to (default: current directory)
    
    Returns:
        tuple: (model_file_path, config_file_path) if successful
        
    Raises:
        Exception: If download fails
    """
    # Ensure download directory exists
    download_path = Path(download_dir)
    download_path.mkdir(parents=True, exist_ok=True)
    
    # Transform model name: replace hyphens with forward slashes
    # e.g., "en_GB-alan-medium" -> "en_GB/alan/medium"
    model_path_segment = model_name.replace('-', '/')
    
    # Construct URLs
    base_url = f"https://huggingface.co/rhasspy/piper-voices/resolve/{version}/en"
    model_url = f"{base_url}/{model_path_segment}/{model_name}.onnx"
    config_url = f"{base_url}/{model_path_segment}/{model_name}.onnx.json"
    
    # Define local file paths
    model_file = download_path / f"{model_name}.onnx"
    config_file = download_path / f"{model_name}.onnx.json"
    
    print(f"Downloading Piper TTS model files for {model_name}...")
    
    try:
        # Download model file
        print(f"Downloading {model_name}.onnx...")
        urllib.request.urlretrieve(model_url, model_file)
        print(f"✓ Downloaded {model_file}")
        
        # Download config file
        print(f"Downloading {model_name}.onnx.json...")
        urllib.request.urlretrieve(config_url, config_file)
        print(f"✓ Downloaded {config_file}")
        
        print("Download complete!")
        return str(model_file), str(config_file)
        
    except urllib.error.URLError as e:
        error_msg = f"Failed to download model files: {str(e)}"
        print(f"✗ {error_msg}")
        
        # Clean up partial downloads
        if model_file.exists():
            model_file.unlink()
        if config_file.exists():
            config_file.unlink()
            
        raise Exception(error_msg)
    except Exception as e:
        error_msg = f"Unexpected error during download: {str(e)}"
        print(f"✗ {error_msg}")
        
        # Clean up partial downloads
        if model_file.exists():
            model_file.unlink()
        if config_file.exists():
            config_file.unlink()
            
        raise Exception(error_msg)


if __name__ == "__main__":
    # Allow the script to be run directly for testing
    import sys
    
    if len(sys.argv) > 1:
        model_name = sys.argv[1]
        version = sys.argv[2] if len(sys.argv) > 2 else "v1.0.0"
        download_dir = sys.argv[3] if len(sys.argv) > 3 else "."
        
        try:
            model_path, config_path = download_models(model_name, version, download_dir)
            print(f"Successfully downloaded:\n  Model: {model_path}\n  Config: {config_path}")
        except Exception as e:
            print(f"Download failed: {e}")
            sys.exit(1)
    else:
        # Download default model
        try:
            model_path, config_path = download_models()
            print(f"Successfully downloaded:\n  Model: {model_path}\n  Config: {config_path}")
        except Exception as e:
            print(f"Download failed: {e}")
            sys.exit(1) 