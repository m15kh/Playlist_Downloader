yt-dlp -f "bestvideo[height<=1080]+bestaudio/best[height<=1080]" \
--write-subs --sub-langs en --convert-subs srt \
--download-sections "*00:44:43-00:44:53" \
--merge-output-format mp4 \
-o "/home/rteam2/m15kh/Playlist_Downloader/section.%(ext)s" \
"https://youtu.be/tArqbPhVQo0?si=7VztSdwv1Q83uIof"
