import os
import subprocess

# Define input and output folders
input_folder = "videos"
output_folder = "output"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Get all .webm files in the videos folder
videos = [f for f in os.listdir(input_folder) if f.endswith(".webm")]

# Loop through all videos
for video in videos:
    # Get filename without extension
    filename = os.path.splitext(video)[0]

    # Define paths for video and subtitle files
    video_path = os.path.join(input_folder, video)
    subtitle_path = os.path.join(input_folder, f"{filename}.en.srt")
    output_path = os.path.join(output_folder, f"{filename}_subtitled.mp4")

    # Check if the subtitle file exists
    if os.path.exists(subtitle_path):
        print(f"Merging subtitles for: {video}")

        # Run ffmpeg command to merge video and subtitles, converting to MP4
        subprocess.run([
            "ffmpeg", "-i", video_path, "-vf", f"subtitles='{subtitle_path}'",
            "-c:v", "libx264", "-crf", "23", "-preset", "fast",
            "-c:a", "aac", "-b:a", "192k", output_path
        ], check=True)
        
        print(f"Saved: {output_path}")
    else:
        print(f"No subtitle found for: {video}")

print("Merging complete! Check the 'output' folder.")
