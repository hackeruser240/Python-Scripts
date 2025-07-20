# filename: copy_paste.py
from pathlib import Path
import re

# File paths
downloads_dir = Path("C:/Users/HP/Downloads")
chat_file = downloads_dir / "chats.txt"
it_links_file = downloads_dir / "it_links.txt" # Adjusted variable name

# Instagram URL pattern
# This pattern aims to capture various Instagram link types including posts, reels, and profiles.
it_pattern = re.compile(r'https?://(?:www\.)?instagram\.com/(?:p|reels|tv|stories|)([a-zA-Z0-9_-]+)(?:/?.*)') # Adjusted regex

# Read and extract Instagram links
with chat_file.open('r', encoding='utf-8') as file:
    lines = file.readlines()

instagram_links = [match.group(0) for line in lines if (match := it_pattern.search(line))] # Changed variable name and group capture

# Write to it_links.txt
with it_links_file.open('w', encoding='utf-8') as file:
    file.write('\n'.join(instagram_links))

print(f"{len(instagram_links)} Instagram link(s) extracted to '{it_links_file.name}'") # Adjusted print statement