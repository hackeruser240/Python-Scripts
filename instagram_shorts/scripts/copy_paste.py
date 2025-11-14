# filename: copy_paste.py
from pathlib import Path
import re
import os # Import os module for checking file size

# File paths
downloads_dir = Path("C:/Users/HP/Downloads")
chat_file = downloads_dir / "chats.txt"
it_links_file = downloads_dir / "it_links.txt" # Adjusted variable name

try:
    # Ensure the downloads directory exists
    if not downloads_dir.exists():
        print(f"Downloads directory '{downloads_dir}' not found. Creating it.")
        downloads_dir.mkdir(parents=True, exist_ok=True)

    # 1. Handle 'chats.txt': Create if it doesn't exist
    if not chat_file.exists():
        print(f"'{chat_file.name}' not found. Creating an empty file at '{chat_file}'.")
        chat_file.touch() # Create the file
        print("Please populate 'chats.txt' with your WhatsApp chat export data and run the script again.")
        # Exit the script as there's no data to process yet
        exit()

    # Read lines from chats.txt
    with chat_file.open('r', encoding='utf-8') as file:
        lines = file.readlines()

    # Instagram URL pattern
    it_pattern = re.compile(r'https?://(?:www\.)?instagram\.com/(?:p|reels|tv|stories|)([a-zA-Z0-9_-]+)(?:/?.*)')

    instagram_links = [match.group(0) for line in lines if (match := it_pattern.search(line))]

    # 2. Handle 'it_links.txt': Check if it exists and is not empty before writing
    if it_links_file.exists() and os.path.getsize(it_links_file) > 0:
        print(f"Error: '{it_links_file.name}' already exists and is not empty. "
              "Please clear its content or delete the file to proceed.")
    else:
        # If it_links_file doesn't exist or is empty, proceed to write
        # 'w' mode will create the file if it doesn't exist, or truncate it if it's empty
        with it_links_file.open('w', encoding='utf-8') as file:
            file.write('\n'.join(instagram_links))
        print(f"{len(instagram_links)} Instagram link(s) extracted to '{it_links_file.name}'")

except FileNotFoundError as e:
    print(f"A file system error occurred: {e}. Please check file paths and permissions.")
except IOError as e:
    print(f"An I/O error occurred while reading/writing files: {e}.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")