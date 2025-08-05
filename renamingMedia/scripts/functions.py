import os
import sys
import argparse as ag # Not used in provided snippet, can be removed if not used elsewhere
import pandas as pd
import fnmatch
import logging
from scripts.variables import AppVariables # Ensure this import is correct

logger = logging.getLogger(__name__)

def loggerSetup(log_file_name: str = AppVariables.LOG_FILE_NAME,
                log_level=AppVariables.LOG_LEVEL, # This can be set to DEBUG
                file_mode: str = AppVariables.LOG_FILE_MODE):
    """
    Sets up the global logger to output messages to both a file and the console (CMD).
    This function now uses logging.basicConfig to configure the root logger,
    which all other loggers (like 'renamingMedia' and 'scripts.functions')
    will inherit from by default.

    Parameters:
    - log_file_name (str): The name of the log file to create in the current working directory.
                           Defaults to "log.txt".
    - log_level (int): The minimum logging level to capture (e.g., logging.INFO, logging.DEBUG).
                       Defaults to logging.INFO.
    - file_mode (str): The mode to open the log file in ('w' for overwrite, 'a' for append).
                       Defaults to 'w'.

    Returns:
    - None: This function configures the global logger instance.
    """
    script_dir = os.getcwd()
    os.makedirs(script_dir, exist_ok=True)

    log_file_path = os.path.join(script_dir, log_file_name)

    # Configure the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # Root logger level set to DEBUG

    # Clear any existing handlers to prevent duplicates
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # Create and add a FileHandler for log.txt with a DEBUG level
    file_handler = logging.FileHandler(log_file_path, mode=file_mode)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%Y %I:%M %p'))
    root_logger.addHandler(file_handler)


def findMedia(media: str, directory: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Identifies and categorizes media files (images or videos) within a specified directory.
    This version converts file extensions to lowercase for robust matching.

    Parameters:
    - media (str): The type of media to search for ('images' or 'videos').
    - directory (str): The path to the directory to scan.

    Returns:
    - tuple[pd.DataFrame, pd.DataFrame]: A tuple containing two pandas DataFrames:
      - df_numbers: Contains files with purely numeric names and their extensions.
      - df_strings: Contains files with alphanumeric or string names and their extensions.
    """
    try:
        # Define expected extensions in lowercase
        if media == AppVariables.MEDIA_TYPE_IMAGES:
            # Use lowercase extensions here, as we'll convert actual file extensions to lowercase
            allowed_extensions = AppVariables.IMAGE_EXTENSIONS
        elif media == AppVariables.MEDIA_TYPE_VIDEOS:
            allowed_extensions = AppVariables.VIDEO_EXTENSIONS
        else:
            logger.error(f"Invalid media type specified: '{media}'. Please choose '{AppVariables.MEDIA_TYPE_IMAGES}' or '{AppVariables.MEDIA_TYPE_VIDEOS}'.")
            sys.exit(1)

        number_names, extension1 = [], []
        string_names, extension2 = [], []

        all_files_in_dir = os.listdir(directory)
        found_media_count = 0

        for filename in all_files_in_dir:
            # Get the file extension and convert it to lowercase for comparison
            name, ext = os.path.splitext(filename)
            ext_lower = ext.lower() # <--- KEY CHANGE HERE

            # Check if the lowercase extension is in our allowed list
            # We also need to add a '*' to the allowed_extensions if they are like '.jpg'
            # Or, more simply, check if ext_lower is in a set of allowed extensions
            if ext_lower in allowed_extensions: # <--- KEY CHANGE HERE
                found_media_count += 1
                if name.isdigit():
                    number_names.append(int(name))
                    extension1.append(ext) # Keep original case for renaming
                else:
                    string_names.append(name)
                    extension2.append(ext) # Keep original case for renaming

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
