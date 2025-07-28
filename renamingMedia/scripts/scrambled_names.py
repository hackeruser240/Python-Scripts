import argparse
import os
import random
import string

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
    # Define common extensions for images and videos
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')
    video_extensions = ('.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm')

    if media_type == 'image':
        extensions_to_scramble = image_extensions
    elif media_type == 'video':
        extensions_to_scramble = video_extensions
    else:
        print(f"Error: Invalid media type '{media_type}'. Please choose 'image' or 'video'.")
        return

    if not os.path.isdir(path):
        print(f"Error: The provided path '{path}' is not a valid directory.")
        return

    scrambled_count = 0
    print(f"Scanning directory: {path} for {media_type} files...")

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
                print(f"Renamed '{filename}' to '{new_filename}'")
                scrambled_count += 1
            except OSError as e:
                print(f"Error renaming '{filename}': {e}")

    print(f"\nFinished scrambling. Total {scrambled_count} {media_type} files scrambled.")

if __name__ == "__main__":
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
