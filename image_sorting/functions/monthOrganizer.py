"""
Script Name: month_folder_organizer.py
Purpose:
    Organize folders named like '01-Jan-2025' into their respective month folders
    inside a given base directory. Then rename those month folders in chronological order
    with numeric prefixes (e.g., '0 January', '1 February', ...).

Behavior:
    - Scans the base directory for folders matching the pattern 'DD-MMM-YYYY'
    - Extracts the month abbreviation and maps it to full month name
    - Moves each folder into its corresponding month folder
    - Renames month folders in calendar order with numeric prefixes

Usage:
    python month_folder_organizer.py --source "E:/Images/Dumps/2025/2025"

Dependencies:
    - Standard Python libraries only (os, shutil, argparse)
"""

import os
import shutil
import argparse
from image_sorting.loggers.LOCAL_loggerSetup import local_loggerSetup

MONTH_MAP = {
    "Jan": "January", "Feb": "February", "Mar": "March", "Apr": "April",
    "May": "May", "Jun": "June", "Jul": "July", "Aug": "August",
    "Sep": "September", "Oct": "October", "Nov": "November", "Dec": "December"
}

MONTH_ORDER = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

def get_month_folder_name(folder_name):
    """Extract month abbreviation and return full month name."""
    parts = folder_name.split("-")
    if len(parts) != 3:
        return None
    month_abbr = parts[1]
    return MONTH_MAP.get(month_abbr)

def move_folder_to_month(folder_name, base_dir):
    """Move folder into its respective month folder."""
    month_full = get_month_folder_name(folder_name)
    if not month_full:
        return False

    src_path = os.path.join(base_dir, folder_name)
    dest_dir = os.path.join(base_dir, month_full)
    dest_path = os.path.join(dest_dir, folder_name)

    try:
        os.makedirs(dest_dir, exist_ok=True)
        shutil.move(src_path, dest_path)
        logger.info(f"✅ Moved: {folder_name} → {month_full}")
        return True
    except Exception as e:
        logger.error(f"⚠️ Error moving {folder_name}: {e}")
        return False

def rename_month_folders(base_dir):
    """Rename month folders in chronological order with numeric prefixes."""
    month_dirs = []
    for folder_name in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder_name)
        if not os.path.isdir(folder_path):
            continue

        # Strip numeric prefix if present
        clean_name = folder_name.split(" ", 1)[-1] if folder_name[0].isdigit() else folder_name
        if clean_name in MONTH_ORDER:
            month_dirs.append(clean_name)

    # Sort by calendar order
    sorted_months = [m for m in MONTH_ORDER if m in month_dirs]

    # Rename folders with numeric prefixes
    for index, month_name in enumerate(sorted_months):
        old_path = os.path.join(base_dir, month_name)
        new_name = f"{index} {month_name}"
        new_path = os.path.join(base_dir, new_name)
        if old_path != new_path:
            try:
                if os.path.exists(new_path):
                    # Merge contents from old_path into new_path
                    for item in os.listdir(old_path):
                        src_item = os.path.join(old_path, item)
                        dest_item = os.path.join(new_path, item)

                        if os.path.exists(dest_item):
                            logger.info(f"⚠️ Skipped: {dest_item} already exists")
                        else:
                            shutil.move(src_item, new_path)

                    os.rmdir(old_path)
                    logger.info(f"🔄 Merged into existing: {new_path}")

                else:
                    os.rename(old_path, new_path)
                    logger.info(f"Renamed: {month_name} → {new_name}")
            except Exception as e:
                logger.error(f"⚠️ Error renaming {month_name}: {e}")

def folders_already_renamed(base_dir):
    """Check if month folders are correctly renamed in calendar order."""
    MONTH_ORDER = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    actual = []
    for folder_name in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder_name)
        if not os.path.isdir(folder_path):
            continue

        parts = folder_name.split(" ", 1)
        if len(parts) == 2 and parts[0].isdigit() and parts[1] in MONTH_ORDER:
            actual.append((int(parts[0]), parts[1]))

    actual.sort()
    expected = [(i, MONTH_ORDER[i]) for i in range(len(actual))]

    return actual == expected

def organize_folders_by_month(base_dir):
    """Scan base directory and organize folders by month."""
    for folder_name in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder_name)
        if not os.path.isdir(folder_path):
            continue
        move_folder_to_month(folder_name, base_dir)
    rename_month_folders(base_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize folders by month.")
    parser.add_argument('--source', type=str, help='Base directory to organize', required=True)
    args = parser.parse_args()

    logger=local_loggerSetup("monthOrganizer.py")
    logger.info(f"Script started with source: {args.source}")
    if args.source:
        organize_folders_by_month(args.source)
    else:
        logger.info("Please provide a valid source directory using --source")