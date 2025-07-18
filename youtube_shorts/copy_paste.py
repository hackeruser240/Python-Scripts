"""
This script reads a WhatsApp chat export file named 'chats.txt' located in the Downloads folder,
extracts all YouTube links from the messages, and writes them to a file named 'yt_links.txt' 
in the same folder.

Only links starting with 'https://youtube.com/' are included. Other links or messages are ignored.
"""

from pathlib import Path
import re

# File paths
downloads_dir = Path("C:/Users/HP/Downloads")
chat_file = downloads_dir / "chats.txt"
yt_links_file = downloads_dir / "yt_links.txt"

# YouTube URL pattern
yt_pattern = re.compile(r'https?://(?:www\.)?youtube\.com/\S+')

# Read and extract YouTube links
with chat_file.open('r', encoding='utf-8') as file:
    lines = file.readlines()

youtube_links = [match.group() for line in lines if (match := yt_pattern.search(line))]

# Write to yt_links.txt
with yt_links_file.open('w', encoding='utf-8') as file:
    file.write('\n'.join(youtube_links))

print(f"{len(youtube_links)} YouTube link(s) extracted to '{yt_links_file.name}'")
