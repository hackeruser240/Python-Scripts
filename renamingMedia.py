import os
import sys
import argparse as ag
import pandas as pd
import fnmatch
import logging

# --- Configure the logger ---
# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(script_dir, "log.txt")

# Create a logger instance
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) # Set the logging level to INFO

# Create file handler which logs even debug messages
# Using 'w' mode to overwrite the log file each time the script runs.
# Change to 'a' if you want to append to the log file.
fh = logging.FileHandler(log_file_path, mode='w')
fh.setLevel(logging.INFO)

# Create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# Add the handlers to the logger
# Clear existing handlers to prevent duplicate logs if run multiple times in an interactive session
if logger.hasHandlers():
    logger.handlers.clear()
logger.addHandler(fh)
logger.addHandler(ch)

# --------------------------------UDF's--------------------------------

def findMedia(media: str, directory: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Identifies and categorizes media files (images or videos) within a specified directory.

    Parameters:
    - media (str): The type of media to search for ('images' or 'videos').
    - directory (str): The path to the directory to scan.

    Returns:
    - tuple[pd.DataFrame, pd.DataFrame]: A tuple containing two pandas DataFrames:
      - df_numbers: Contains files with purely numeric names and their extensions.
      - df_strings: Contains files with alphanumeric or string names and their extensions.
    """
    try:
        if media in ['images', 'image']:
            extensions = ('*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.tiff')
        elif media in ['video', 'videos']:
            extensions = ('*.mp4', '*.mpeg', '*.mkv', '*.avi', '*.mov', '*.wmv', '*.flv')
        else:
            logger.error(f"Invalid media type specified: '{media}'. Please choose 'images' or 'videos'.")
            sys.exit(1)

        number_names, extension1 = [], []
        string_names, extension2 = [], []

        all_files_in_dir = os.listdir(directory)
        found_media_count = 0

        for ext_pattern in extensions:
            for filename in fnmatch.filter(all_files_in_dir, ext_pattern):
                found_media_count += 1
                name = os.path.splitext(filename)[0]
                ext = os.path.splitext(filename)[1]

                if name.isdigit():
                    number_names.append(int(name))
                    extension1.append(ext)
                else:
                    string_names.append(name)
                    extension2.append(ext)

        df_numbers = pd.DataFrame({"Filenames": number_names, "Extensions": extension1})
        df_strings = pd.DataFrame({"Filenames": string_names, "Extensions": extension2})
        logger.info(f"Found {found_media_count} {media} file(s) in '{directory}'.")
        logger.info(f"Total {len(all_files_in_dir) - found_media_count} non-{media} file(s) are present in the directory and will be ignored.")
        return df_numbers, df_strings
    except FileNotFoundError:
        logger.error(f"Error: Directory not found at '{directory}'. Please check the path.")
        sys.exit(1)
    except PermissionError:
        logger.error(f"Error: Permission denied to access directory '{directory}'.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred in findMedia: {e}")
        sys.exit(1)

def findingBreakingPoint(mylist: list) -> int:
    """
    Identifies the index where a sequential numeric list breaks its continuity.

    Parameters:
    - mylist (list): A list of numbers, expected to be sorted.

    Returns:
    - int: The index of the element before the break. Returns -1 if the list
           has less than 2 elements, or if no break is found (meaning the list is continuous).
    """
    if len(mylist) < 2:
        return -1

    for u in range(len(mylist) - 1):
        if mylist[u+1] == mylist[u] + 1:
            pass
        else:
            logger.info(f"Sequence break detected: {mylist[u]} followed by {mylist[u+1]} at index {u}.")
            return u
    return len(mylist) - 1 # If no break, return the last index

def renamingFiles(final_df: pd.DataFrame, directory_path: str):
    """
    Renames files based on the 'Filenames', 'Extensions', and 'New names' columns
    in the provided DataFrame.

    Parameters:
    - final_df (pd.DataFrame): A DataFrame containing 'Filenames', 'Extensions',
                                and 'New names' columns for all files to be renamed.
    - directory_path (str): The base directory where the files are located.

    Returns:
    - None: Performs file renaming operations directly.
    """
    if final_df.empty:
        logger.info("No files to rename in the final DataFrame.")
        return

    logger.info("\n" + "="*40 + "\nStarting file renaming process...\n" + "="*40)
    for index, row in final_df.iterrows():
        try:
            original_filename = str(row['Filenames']) + row['Extensions']
            new_filename = str(row['New names']) + row['Extensions']

            current_src_path = os.path.join(directory_path, original_filename)
            current_dst_path = os.path.join(directory_path, new_filename)

            if not os.path.exists(current_src_path):
                logger.warning(f"Warning: Source file not found, skipping: '{current_src_path}'")
                continue

            if current_src_path == current_dst_path:
                logger.info(f"Skipping: '{original_filename}' is already correctly named as '{new_filename}'.")
                continue

            # Check if the destination file already exists and is different from source
            if os.path.exists(current_dst_path) and current_src_path != current_dst_path:
                logger.error(f"Error: Cannot rename '{original_filename}' to '{new_filename}'. "
                             f"Destination file '{current_dst_path}' already exists and is different from source.")
                continue # Skip this specific rename to avoid collision

            os.rename(current_src_path, current_dst_path)
            logger.info(f"Renamed '{original_filename}' to '{new_filename}'")

        except FileNotFoundError:
            logger.error(f"Error: File not found during renaming. Source: '{current_src_path}', Destination: '{current_dst_path}'")
        except PermissionError:
            logger.error(f"Error: Permission denied during renaming. Check file permissions for '{current_src_path}' or '{current_dst_path}'.")
        except OSError as e:
            logger.error(f"OS Error during renaming '{original_filename}' to '{new_filename}': {e}")
        except KeyError as e:
            logger.error(f"DataFrame key error during renaming: Missing column {e}. Ensure 'Filenames', 'Extensions', 'New names' exist.")
        except Exception as e:
            logger.error(f"An unexpected error occurred during renaming file '{original_filename}': {e}")

def renamingStrings(strings_df: pd.DataFrame, starting_point_for_strings: int) -> pd.DataFrame:
    """
    Assigns new sequential numeric names to files that originally had string names.
    The numbering starts from a specified point, typically after the last numeric file.

    Parameters:
    - strings_df (pd.DataFrame): DataFrame containing string-named files and their extensions.
    - starting_point_for_strings (int): The integer value from which to start numbering
                                        the string-named files.

    Returns:
    - pd.DataFrame: The updated strings_df with a new 'New names' column containing
                    the assigned sequential numeric names.
    """
    if strings_df.empty:
        logger.info("No string-named files to process for renaming.")
        return strings_df

    try:
        # Ensure 'New names' column exists before assigning
        if 'New names' not in strings_df.columns:
            strings_df['New names'] = pd.NA # Initialize with pandas Not Available

        for i in range(len(strings_df)):
            strings_df.loc[i, 'New names'] = starting_point_for_strings + i

        strings_df['New names'] = strings_df['New names'].astype("Int64") # Use Int64 for nullable integer
        logger.info("="*40)
        logger.info("Strings DataFrame after assigning new names:")
        logger.info(strings_df.head())
        logger.info("="*40)
        return strings_df
    except Exception as e:
        logger.error(f"Error in renamingStrings function: {e}")
        return strings_df # Return the original DataFrame in case of error

def main():
    """
    Main function to parse arguments, find media, process names, and rename files.
    """
    parser = ag.ArgumentParser(description='''
    This script helps in renaming media (images or video) in a given directory!
    ''')

    parser.add_argument("--path", required=True, type=str, help='Enter the directory in which you want your images or videos renamed')
    parser.add_argument("--media", required=True, type=str, choices=['images', 'videos'], help='Select the type of media.')
    args = parser.parse_args()

    path = rf'{args.path}'
    media = rf'{args.media}'

    logger.info(f"Script started for path: '{path}' and media type: '{media}'")

    # 1. Find and categorize media files
    numbers_df, strings_df = findMedia(media, path)

    logger.info("\n" + "="*40 + "\nInitial DataFrames:\n" + "="*40)
    logger.info("DataFrame 'numbers' initial:\n" + str(numbers_df.head()))
    logger.info("DataFrame 'strings' initial:\n" + str(strings_df.head()))

    max_existing_number = 0

    # 2. Process numeric files
    if not numbers_df.empty:
        try:
            # Sort numeric files by their current names
            numbers_df = numbers_df.sort_values(by='Filenames', ascending=True, ignore_index=True)

            # Generate new sequential names for numeric files
            existing_numeric_names_set = set(numbers_df['Filenames'].tolist())
            new_names_for_numbers = []
            current_expected_number = 1

            for index, row in numbers_df.iterrows():
                # If the current filename is already the expected sequential number, keep it
                if row['Filenames'] == current_expected_number:
                    new_names_for_numbers.append(current_expected_number)
                    current_expected_number += 1
                else:
                    # If there's a gap or a non-sequential number, assign the next available unique number
                    # This loop ensures the assigned number is not already taken by an existing file
                    while current_expected_number in existing_numeric_names_set:
                        current_expected_number += 1
                    new_names_for_numbers.append(current_expected_number)
                    current_expected_number += 1

            numbers_df['New names'] = new_names_for_numbers
            logger.info("\n" + "="*40 + "\nDataFrame 'numbers' with 'New names':\n" + "="*40)
            logger.info(numbers_df.to_string()) # Use to_string() to show all rows

            max_existing_number = numbers_df['New names'].max()
        except Exception as e:
            logger.error(f"Error processing numeric files: {e}")
            sys.exit(1)
    else:
        logger.info("There are no numeric filenames in the given path!")
        max_existing_number = 0 # If no numeric files, start string numbering from 1

    # 3. Determine starting point for string files
    starting_point_for_strings = max_existing_number + 1
    logger.info(f"Starting point for renaming string files: {starting_point_for_strings}")

    # 4. Process string files
    if not strings_df.empty:
        strings_df = renamingStrings(strings_df, starting_point_for_strings)
    else:
        logger.info("Not processing any string names!")

    # 5. Combine both DataFrames
    final_df = pd.DataFrame()
    if numbers_df.empty and strings_df.empty:
        logger.info("No media files found to rename.")
    elif numbers_df.empty:
        final_df = strings_df
    elif strings_df.empty:
        final_df = numbers_df
    else:
        try:
            final_df = pd.concat([numbers_df, strings_df], ignore_index=True)
            # Ensure 'New names' column is integer type in the combined DataFrame
            final_df['New names'] = final_df['New names'].astype("Int64")
        except Exception as e:
            logger.error(f"Error concatenating DataFrames: {e}")
            sys.exit(1)

    # Sort final DataFrame by 'New names' to ensure correct processing order
    if not final_df.empty:
        try:
            final_df = final_df.sort_values(by='New names', ascending=True, ignore_index=True)
        except KeyError:
            logger.error("Error: 'New names' column missing in final DataFrame during sorting.")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Error sorting final DataFrame: {e}")
            sys.exit(1)

    logger.info("\n" + "="*40 + "\nFinal combined DataFrame for renaming:\n" + "="*40)
    logger.info(final_df.to_string()) # Use to_string() to show all rows

    # 6. Finally rename the files
    renamingFiles(final_df, path)

    logger.info("\n" + "="*40 + "\nScript execution finished.\n" + "="*40)

# Entry point for the script
if __name__ == "__main__":
    main()