import os
import logging
from telegram import Bot
from telegram.error import TelegramError
import asyncio
from pathlib import Path

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Telegram Bot Configuration
TOKEN = "7567782899:AAE13__OXTxaVaIqi8eQBiN6X0x6mhzByRk"  # Replace with your bot token
CHANNEL_ID = "@umarjamilai"  # Replace with your channel username or ID

async def upload_video(bot, video_path):
    """Upload a single video to Telegram channel"""
    try:
        with open(video_path, 'rb') as video_file:
            await bot.send_video(
                chat_id=CHANNEL_ID,
                video=video_file,
                caption=Path(video_path).stem,  # Use filename as caption
                supports_streaming=True
            )
        logger.info(f"Successfully uploaded: {video_path}")
        return True
    except TelegramError as e:
        logger.error(f"Failed to upload {video_path}: {e}")
        return False

async def upload_videos_from_folder(folder_path):
    """Upload all videos from a specified folder"""
    # Initialize bot
    bot = Bot(token=TOKEN)
    
    # Supported video formats
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
    
    # Get all video files
    video_files = []
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path) and os.path.splitext(file)[1].lower() in video_extensions:
            video_files.append(file_path)
    
    if not video_files:
        logger.warning(f"No video files found in {folder_path}")
        return
    
    logger.info(f"Found {len(video_files)} videos to upload")
    
    # Upload each video
    for video_path in video_files:
        await upload_video(bot, video_path)
        # Sleep to avoid hitting rate limits
        await asyncio.sleep(2)

async def main():
    # Path to the folder containing videos
    videos_folder = "/home/rteam2/m15kh/playlist-downloader/output"  # Replace with your folder path
    
    await upload_videos_from_folder(videos_folder)

if __name__ == "__main__":
    asyncio.run(main())
