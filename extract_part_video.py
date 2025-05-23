from moviepy.video.io.VideoFileClip import VideoFileClip
import os

def time_str_to_seconds(t):
    h, m, s = map(int, t.split(":"))
    return h * 3600 + m * 60 + s

def extract_and_rename(input_path, start_time_str, end_time_str):
    base_name = os.path.basename(input_path)
    
    # Convert time strings to seconds
    start_time = time_str_to_seconds(start_time_str)
    end_time = time_str_to_seconds(end_time_str)
    
    # Format times for filename
    start_str = start_time_str.replace(":", "-")
    end_str = end_time_str.replace(":", "-")
    
    output_name = f"split_{start_str}_to_{end_str}_{base_name}"
    
    with VideoFileClip(input_path) as video:
        subclip = video.subclip(start_time, end_time)
        subclip.write_videofile(output_name, codec="libx264")
    
    os.remove(input_path)
    print(f"Saved extracted part as {output_name} and deleted original video.")

# Example usage:
input_video = "filename.mp4"  # Change to your video file name
start = "00:03:55"         # Your start time
end = "00:05:45"           # Your end time

extract_and_rename(input_video, start, end)
