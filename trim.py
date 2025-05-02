import subprocess
import os

def trim_video(input_path: str, start_time: str, end_time: str, output_path: str = None) -> str:
    """
    Trim a video file between start_time and end_time using ffmpeg.

    Parameters:
        input_path (str): Path to the input video file.
        start_time (str): Start time in format HH:MM:SS (e.g., '00:01:30').
        end_time (str): End time in format HH:MM:SS (e.g., '00:01:40').
        output_path (str): Optional output path. If None, adds '_trimmed' to the input filename.

    Returns:
        str: Path to the trimmed video file.

    Raises:
        FileNotFoundError: If the input file doesn't exist.
        RuntimeError: If ffmpeg fails to trim the video.
    """
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input video not found: {input_path}")

    if output_path is None:
        base, ext = os.path.splitext(input_path)
        # Replace colons with underscores for a valid filename
        start_time_clean = start_time.replace(":", "_")
        end_time_clean = end_time.replace(":", "_")
        output_path = f"{base}_{start_time_clean}to{end_time_clean}_trimmed{ext}"

    cmd = [
        "ffmpeg",
        "-ss", start_time,
        "-to", end_time,
        "-i", input_path,
        "-c", "copy",  # copy streams without re-encoding
        "-y",  # overwrite output file if it exists
        output_path
    ]

    print(f"[INFO] Trimming video from {start_time} to {end_time}...")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        error_msg = result.stderr.decode()
        print("[ERROR] ffmpeg failed:\n", error_msg)
        raise RuntimeError("ffmpeg trimming failed")

    print(f"[SUCCESS] Trimmed video saved to: {output_path}")
    return output_path


# Example usage
trim_video("full.mp4", "00:22:41", "00:23:00")
