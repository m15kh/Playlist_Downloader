import whisper
import yaml
import os
import pathlib
import json

# Helper function to format timestamps for SRT file
def format_timestamp(seconds):
    """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)"""
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    secs = int(seconds % 60)
    millisecs = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"

# Read configuration from YAML file
with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

# Get model name and audio path from config
model_name = config["model"]
audio_path = config["audio_path"]

# Create output directory based on audio filename
audio_filename = os.path.basename(audio_path)
audio_name = os.path.splitext(audio_filename)[0]  # Get name without extension
output_dir = f"result_wisper/{audio_name}_srt"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Load the specified model
model = whisper.load_model(model_name)

# Transcribe the full audio with word timestamps
print(f"Transcribing audio with model: {model_name}")
try:
    result = model.transcribe(
        audio_path,
        word_timestamps=True,  # Enable word-by-word timestamps
        verbose=True           # Show progress
    )
    word_timestamps_enabled = True
except AttributeError as e:
    # Handle the specific Triton error related to src attribute
    if "Cannot set attribute 'src' directly" in str(e):
        print("Warning: Word timestamps not supported with this configuration. Falling back to basic transcription.")
        result = model.transcribe(
            audio_path,
            word_timestamps=False,  # Disable word-by-word timestamps
            verbose=True           # Show progress
        )
        word_timestamps_enabled = False
    else:
        # Re-raise if it's a different AttributeError
        raise

# Get the detected language
detected_language = result["language"]
print(f"Detected language: {detected_language}")

# Save the full recognized text to a txt file
with open(f"{output_dir}/{audio_name}.txt", "w", encoding="utf-8") as text_file:
    text_file.write(result["text"])

# Save word-by-word results to a JSON file (includes timestamps for each word)
import json
with open(f"{output_dir}/{audio_name}_words.json", "w", encoding="utf-8") as word_file:
    json.dump(result, word_file, indent=2, ensure_ascii=False)

# Generate and save SRT subtitle file
with open(f"{output_dir}/{audio_name}.srt", "w", encoding="utf-8") as srt_file:
    # Extract segments with timestamps
    segments = result["segments"]
    
    for i, segment in enumerate(segments):
        # Get start and end time in SRT format (HH:MM:SS,mmm)
        start_time = format_timestamp(segment["start"])
        end_time = format_timestamp(segment["end"])
        
        # Write SRT entry
        srt_file.write(f"{i+1}\n")
        srt_file.write(f"{start_time} --> {end_time}\n")
        srt_file.write(f"{segment['text'].strip()}\n\n")

# Generate word-by-word text file with timestamps
if word_timestamps_enabled:
    with open(f"{output_dir}/{audio_name}_word_timestamps.txt", "w", encoding="utf-8") as word_ts_file:
        for segment in result["segments"]:
            if "words" in segment:
                for word_data in segment["words"]:
                    word = word_data["word"]
                    start = word_data["start"]
                    end = word_data["end"]
                    word_ts_file.write(f"[{start:.2f}-{end:.2f}] {word}\n")
            word_ts_file.write("\n")
else:
    print("Word timestamps not available - skipping word timestamp file generation")

# Print the output directory and recognized text
print(f"Output saved to: {output_dir}")
print(result["text"])