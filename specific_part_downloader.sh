#!/bin/bash

# --- CONFIGURABLE VARIABLES ---
URL="https://youtu.be/tArqbPhVQo0?si=7VztSdwv1Q83uIof"
VIDEO_FORMAT="270"  # 1080p video
AUDIO_FORMAT="234"  # audio stream
FULL_OUTPUT="full.mp4"
CLIP_OUTPUT="section.mp4"
START_TIME="00:44:43"
END_TIME="00:44:53"

# --- DOWNLOAD FULL VIDEO ---
echo "[INFO] Downloading full video..."
yt-dlp -f "${VIDEO_FORMAT}+${AUDIO_FORMAT}" --merge-output-format mp4 -o "$FULL_OUTPUT" "$URL"
if [ $? -ne 0 ]; then
    echo "[ERROR] yt-dlp failed. Aborting."
    exit 1
fi

# --- TRIM SECTION USING FFMPEG ---
echo "[INFO] Trimming clip from $START_TIME to $END_TIME..."
ffmpeg -ss "$START_TIME" -to "$END_TIME" -i "$FULL_OUTPUT" -c copy "$CLIP_OUTPUT"
if [ $? -ne 0 ]; then
    echo "[ERROR] ffmpeg failed to create the clip."
    exit 1
fi

echo "[SUCCESS] Clip saved as $CLIP_OUTPUT"
