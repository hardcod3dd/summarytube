import yt_dlp
import os
import subprocess
from openai import OpenAI

client = OpenAI(api_key="")

def download_yt(url):
    URLS = [url]

    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'output': 'yt.m4a',
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
     }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(URLS)

def rename_convert():
    current_folder = os.getcwd()  # Get the current working directory
    files = os.listdir(current_folder)  # List all files in the current directory

    for file in files:
        if file.endswith(".m4a"):  # Check if the file has a .m4a extension
            old_path = os.path.join(current_folder, file)
            new_path = os.path.join(current_folder, "output.m4a")

            os.rename(old_path, new_path)

    subprocess.run('ffmpeg -i output.m4a -acodec pcm\_s16le -ac 1 -ar 16000 output.wav', shell=True, check=True)

def extract_text(lang):
    subprocess.run(f'whisper.cpp/main -l {lang} -m whisper.cpp/models/ggml-large-v3.bin -nt -otxt -f output.wav', shell=True, check=True)

# Function to analyze sentiment using ChatGPT
def summarize(lang):
    with open('output.wav.txt', 'r') as dosya:
        text = dosya.read()

    system_msg = "You are a helpful assistant."
    user_msg = f"Summarize this text please. : \"{text}\"."
    response = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"Please summarize the following text in {lang} using bulletpoints :\n{text}\n\nSummary:",
        }
    ],
    model="gpt-3.5-turbo",
)
    summary = response.choices[0].message.content
    return summary

def cleanup():
    files_to_remove = ['output.m4a', 'output.wav', 'output.wav.txt']
    for file_name in files_to_remove:
        file_path = os.path.join(os.getcwd(), file_name)
    
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"File '{file_name}' removed successfully.")
            except OSError as e:
                print(f"Error removing file '{file_name}': {e}")
        else:
            pass

if __name__ == "__main__":
    cleanup()
    yt_url = input("Enter the url for your file: ")
    language = input("Enter the language code for the video (tr,en,de,auto) : ")
    final_lang = input("Enter the final results language (Turkish,English,German) :")
    download_yt(yt_url)
    rename_convert()
    extract_text(language)
    print('This might take some time.')
    print(summarize(final_lang))
