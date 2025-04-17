from moviepy.editor import VideoFileClip
import math
import os

def split_video(video_path, output_dir, segment_length=180):  # 180 seconds = 3 minutes
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    clip = VideoFileClip(video_path)
    video_duration = clip.duration

    # Calculate number of segments
    num_segments = math.ceil(video_duration / segment_length)

    for i in range(num_segments):
        start_time = i * segment_length
        end_time = min((i + 1) * segment_length, video_duration)

        # Extract segment
        segment_clip = clip.subclip(start_time, end_time)

        # Save segment
        output_filename = os.path.join(output_dir, f"segment_{i+1}.mp4")
        segment_clip.write_videofile(output_filename, codec="libx264")

    clip.close()

# Example usage
video_file = "How to Build Endurance ｜ Huberman Lab Essentials [7MEhDlw1e9k].mp4"
output_folder = "output/"
split_video(video_file, output_folder)