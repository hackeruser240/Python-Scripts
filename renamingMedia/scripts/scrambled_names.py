import argparse
import os
import random
import string
import logging
import sys

# Initialize logger for this module
logger = logging.getLogger(__name__)

# No need for setup_standalone_logger or setup_module_logger here
# as logging will be configured by the main application (gui_app.py)

def generate_random_name(length=15):
    """Generates a random alphanumeric string of a specified length."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def scramble_media_names(path, media_type):
    """
    Scrambles (renames) media files in the given path based on media_type.

    Args:
        path (str): The directory path containing the media files.
        media_type (str): The type of media to scramble ('image' or 'video').
    """
    logger.info("Starting to scramble names...")
    # Define common extensions for images and videos
    # These should ideally come from a centralized config like AppVariables
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heic', '.jfif')
    video_extensions = ('.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm', '.mpeg')

    if media_type == 'image':
        extensions_to_scramble = image_extensions
    elif media_type == 'video':
        extensions_to_scramble = video_extensions
    else:
        logger.error(f"Error: Invalid media type '{media_type}'. Please choose 'image' or 'video'.")
        return

    if not os.path.isdir(path):
        logger.error(f"Error: The provided path '{path}' is not a valid directory.")
        return

    scrambled_count = 0
    logger.info(f"Scanning directory: {path} for {media_type} files...")

    for filename in os.listdir(path):
        # Get the full path of the file
        file_path = os.path.join(path, filename)

        # Check if it's a file and has one of the target extensions (case-insensitive)
        if os.path.isfile(file_path) and filename.lower().endswith(extensions_to_scramble):
            # Split filename into base and extension
            base_name, extension = os.path.splitext(filename)

            # Generate a new random name
            new_base_name = generate_random_name()
            new_filename = new_base_name + extension
            new_file_path = os.path.join(path, new_filename)

            # Ensure the new name doesn't already exist (highly unlikely with random names, but good practice)
            while os.path.exists(new_file_path):
                new_base_name = generate_random_name()
                new_filename = new_base_name + extension
                new_file_path = os.path.join(path, new_filename)

            try:
                os.rename(file_path, new_file_path)
                logger.debug(f"Renamed '{filename}' to '{new_filename}'") # DEBUG messages
                scrambled_count += 1
            except OSError as e:
                logger.info(f"Error renaming '{filename}': {e}") # INFO for errors during renaming

    logger.info(f"Finished scrambling. Total {scrambled_count} {media_type} files scrambled.")

if __name__ == "__main__":
    # This block is for standalone execution of scrambled_names.py
    # If run via the GUI, this block will not be executed.
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%Y %I:%M %p')

    # Console handler for standalone INFO output
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)

    # File handler for standalone DEBUG output
    file_handler = logging.FileHandler('scramble_standalone_log.txt', mode='a')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    logger.info("Running scrambled_names.py in standalone mode.")

    parser = argparse.ArgumentParser(
        description="Scramble (rename) image or video files in a specified directory to random alphanumeric names."
    )
    parser.add_argument(
        "path",
        type=str,
        help="The path to the directory containing the media files."
    )
    parser.add_argument(
        "media_type",
        type=str,
        choices=['image', 'video'],
        help="The type of media to scramble: 'image' or 'video'."
    )

    args = parser.parse_args()

    scramble_media_names(args.path, args.media_type)

