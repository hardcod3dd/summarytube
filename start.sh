#!/bin/bash
# Check if the folder exists
if [ -d "whisper.cpp" ]; then
    echo "'$repo_name' already exists. Skipping install."
else
    # Clone the GitHub repository
    repo_url="https://github.com/ggerganov/whisper.cpp"
    git clone "$repo_url"

    # Check if the cloning was successful
    if [ $? -eq 0 ]; then
        cd "whisper.cpp" || make
        clear
        echo "Installed successfully.Now downloading the models."
        bash ./whisper.cpp/models/download-ggml-model.sh large-v3
    else
        echo "Install failed."
    fi
fi

clear

python3 main.py
