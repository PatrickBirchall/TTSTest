#!/bin/bash

# Define model name and version
MODEL="en_US-lessac-medium"
VERSION="v1.2.0"

# Define URLs for model and config files
MODEL_URL="https://github.com/rhasspy/piper/releases/download/${VERSION}/${MODEL}.onnx"
CONFIG_URL="https://github.com/rhasspy/piper/releases/download/${VERSION}/${MODEL}.onnx.json"

echo "Downloading Piper TTS model files..."

# Download model file
echo "Downloading ${MODEL}.onnx..."
curl -L -o "${MODEL}.onnx" "$MODEL_URL"

# Download config file
echo "Downloading ${MODEL}.onnx.json..."
curl -L -o "${MODEL}.onnx.json" "$CONFIG_URL"

echo "Download complete!"
