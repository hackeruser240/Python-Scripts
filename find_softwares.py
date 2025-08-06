import os
import logging

def find_softwares(directory_path):
    """
    Scans the given directory and its subdirectories for files with .exe or .msi extensions.

    Args:
        directory_path (str): The path to the directory to scan.

    Returns:
        list: A list of full paths to the found software files.
    """
    software_files = []
    if not os.path.exists(directory_path):
        logger.error(f"Error: Directory '{directory_path}' does not exist.")
        return software_files
    
    logger.info(f"Scanning directory: {directory_path}")

    # Walk through the directory and its subdirectories
    for entry in os.listdir(directory_path):
        full_path = os.path.join(directory_path, entry)
        if os.path.isfile(full_path):
            software_files.append(entry)
        else:
            pass
    return software_files

def main(target_directory):
    """
    Main function to run the software finder script.
    """
    # Specify the directory you want to scan
    target_directory = rf"{target_directory}" # Using a raw string (r"...") to handle backslashes correctly

    # Find the software files
    found_softwares = find_softwares(target_directory)

    # Print the results
    if found_softwares:
        logger.info("\nFound software files:")
        for software in found_softwares:
            logger.info(software)
        logger.info(f"Total {len(software)} softwares found.")
    else:
        logger.debug("\nNo software files (.exe or .msi) found in the specified directory.")

def loggerSetup():
    logger=logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter=logging.Formatter( '%(asctime)s - %(name)s - %(levelname)s - %(message)s',datefmt='%d-%b-%Y %I:%M %p' )

    #Handler:
    helper=logging.StreamHandler()
    helper.setLevel(logging.INFO)
    helper.setFormatter(formatter)    
    
    logger.addHandler(helper)
    return logger

if __name__ == "__main__":
    logger=loggerSetup()
    target_directory=r"D:\Softwares"
    main(target_directory)