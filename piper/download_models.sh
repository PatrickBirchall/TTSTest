#!/bin/bash

# Define model name and version
MODEL="en_US-lessac-high"
VERSION="v1.0.0"

# Define URLs for model and config files
#MODEL_URL="https://huggingface.co/rhasspy/piper-voices/resolve/${VERSION}/en/en_GB/northern_english_male/medium/${MODEL}"
#CONFIG_URL="https://huggingface.co/rhasspy/piper-voices/resolve/${VERSION}/en/en_GB/northern_english_male/medium/${MODEL}.json"

MODEL_URL="https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/$(echo ${MODEL} | sed 's/-/\//g')/${MODEL}.onnx"
CONFIG_URL="https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/$(echo ${MODEL} | sed 's/-/\//g')/${MODEL}.onnx.json"

echo "Downloading Piper TTS model files..."

# Download model file
echo "Downloading ${MODEL}.onnx..."
curl -L -o "${MODEL}.onnx" "$MODEL_URL"

# Download config file
echo "Downloading ${MODEL}.onnx.json..."
curl -L -o "${MODEL}.onnx.json" "$CONFIG_URL"

echo "Download complete!"
