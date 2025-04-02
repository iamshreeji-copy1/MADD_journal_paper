import os
import multiprocessing
from pydub import AudioSegment
from tqdm import tqdm  # For progress tracking

# Define base directories
BASE_DIR = "/media/linux/Seagate/Arth_dharmendra_ravindra_journal/website/wavs"
OUTPUT_DIR = os.path.join(BASE_DIR, "mp3s")

# Create the output directory if it does not exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Collect all WAV files
wav_files = []
for root, _, files in os.walk(BASE_DIR):
    for file in files:
        if file.endswith(".wav"):
            wav_files.append(os.path.join(root, file))

# Function to convert a single WAV to MP3
def convert_wav_to_mp3(wav_path):
    try:
        # Get the relative path for preserving folder structure
        relative_path = os.path.relpath(wav_path, BASE_DIR)
        mp3_path = os.path.join(OUTPUT_DIR, os.path.splitext(relative_path)[0] + ".mp3")
        
        # Create output folder if needed
        os.makedirs(os.path.dirname(mp3_path), exist_ok=True)

        # Convert WAV to MP3
        audio = AudioSegment.from_wav(wav_path)
        audio.export(mp3_path, format="mp3", bitrate="192k")  # High quality

        return f"✅ Converted: {wav_path} → {mp3_path}"

    except Exception as e:
        # Log errors in a file
        with open("error_log.txt", "a") as log_file:
            log_file.write(f"❌ Failed: {wav_path} | Error: {str(e)}\n")
        return f"❌ Failed: {wav_path} | Error: {str(e)}"

# Use multiprocessing for faster conversion
if __name__ == "__main__":
    print(f"🔍 Found {len(wav_files)} WAV files. Starting conversion...")

    # Use multiprocessing to speed up the process
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = list(tqdm(pool.imap(convert_wav_to_mp3, wav_files), total=len(wav_files)))

    print("\n🎉 Conversion Complete! Check 'error_log.txt' for any failed files.")
