import os
import sys
import argparse as ag
import pandas as pd
import fnmatch
import logging

from scripts.functions import (
    loggerSetup,
    findMedia,
    findingBreakingPoint,
    renamingFiles,
    renamingStrings )



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

    
    # Call loggerSetup once at the beginning to configure the logger
    loggerSetup()

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
    # Global logger instance (will be configured by loggerSetup)
    logger = logging.getLogger(__name__)

    main()