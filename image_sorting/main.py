import shutil, os
from image_sorting.functions.imageSorting import *
from image_sorting.functions.monthOrganizer import organize_folders_by_month
from image_sorting.loggers.APP_loggerSetup import app_loggerSetup

def snapchat():
    SRC = r"E:\Phone Backups\Snapchat"
    DST = r"E:\Images\Snapchat"

    if os.path.exists( os.path.join(DST, "2024") ):
        shutil.rmtree( os.path.join(DST, "2024") )
        logger.info(f"Deleted existing folder: {os.path.join(DST, '2024')}")
            
    if os.path.exists( os.path.join(DST, "2025") ):
        shutil.rmtree( os.path.join(DST, "2025") )
        logger.info(f"Deleted existing folder: {os.path.join(DST, '2025')}")

    # Copy the backup
    if os.path.isdir(SRC):
        os.makedirs(DST, exist_ok=True)
        for item in os.listdir(SRC):
            src_item = os.path.join(SRC, item)
            dst_item = os.path.join(DST, item)
            if os.path.isdir(src_item):
                shutil.copytree(src_item, dst_item, dirs_exist_ok=True)
            else:
                shutil.copy2(src_item, dst_item)
                logger.info(f"Copied file: {src_item} to {dst_item}")
        logger.info("Snapchat copied successfully.")
    else:
        logger.info(f"Source folder not found: {SRC}")

    #imageSorting()
    IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png')
    VIDEO_EXTENSIONS = ('.mp4', '.mkv', '.mov', '.avi', '.m4a', '.webm')
    SUPPORTED_EXTENSIONS = IMAGE_EXTENSIONS + VIDEO_EXTENSIONS

    
    for filename in os.listdir(DST):
        if not filename.lower().endswith(SUPPORTED_EXTENSIONS):
            continue

        full_path = os.path.join(DST, filename)
        creation_date = get_file_creation_date(full_path)

        if creation_date:
            destination_folder = build_destination_path(DST, creation_date)
            copy_and_move_to_raw(full_path, destination_folder)
        else:
            logger.info(f"Skipped (no date found): {filename}")

    #monthOrganizer()
    dst=os.path.join(DST, "2025")
    organize_folders_by_month(dst)

    dst=os.path.join(DST, "2024")
    organize_folders_by_month(dst)

def whatsapp():

    SRC = r"E:\Phone Backups\WhatsApp Images"
    DST = r"E:\Images\WhatsApp dumps\2025"

    if os.path.exists( os.path.join(DST, "2024") ):
        shutil.rmtree( os.path.join(DST, "2024") )
        logger.info(f"Deleted existing folder: {os.path.join(DST, '2024')}")
            
    if os.path.exists( os.path.join(DST, "2025") ):
        shutil.rmtree( os.path.join(DST, "2025") )
        logger.info(f"Deleted existing folder: {os.path.join(DST, '2025')}")

    # Copy the backup
    if os.path.isdir(SRC):
        os.makedirs(DST, exist_ok=True)
        for item in os.listdir(SRC):
            if item == ".stfolder":
                continue  # Skip the .stfolder directory
            src_item = os.path.join(SRC, item)
            dst_item = os.path.join(DST, item)
            if os.path.isdir(src_item):
                shutil.copytree(src_item, dst_item, dirs_exist_ok=True)
            else:
                shutil.copy2(src_item, dst_item)
                logger.info(f"Copied file: {src_item} to {dst_item}")
        logger.info("Snapchat copied successfully.")
    else:
        logger.info(f"Source folder not found: {SRC}")

    #imageSorting()
    IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png')
    VIDEO_EXTENSIONS = ('.mp4', '.mkv', '.mov', '.avi', '.m4a', '.webm')
    SUPPORTED_EXTENSIONS = IMAGE_EXTENSIONS + VIDEO_EXTENSIONS

    
    for filename in os.listdir(DST):
        if not filename.lower().endswith(SUPPORTED_EXTENSIONS):
            continue

        full_path = os.path.join(DST, filename)
        creation_date = get_file_creation_date(full_path)

        if creation_date:
            destination_folder = build_destination_path(DST, creation_date)
            copy_and_move_to_raw(full_path, destination_folder)
        else:
            logger.info(f"Skipped (no date found): {filename}")

    #monthOrganizer()
    dst=os.path.join(DST, "2025")
    organize_folders_by_month(dst)

    dst=os.path.join(DST, "2024")
    organize_folders_by_month(dst)

def whatsapp_SENT():
    
    SRC = r"E:\Images\WhatsApp dumps\2025\Sent"
    #DST = r"E:\Images\WhatsApp dumps\2025"

    if os.path.exists( os.path.join(SRC, "2024") ):
        shutil.rmtree( os.path.join(SRC, "2024") )
        logger.info(f"Deleted existing folder: {os.path.join(SRC, '2024')}")
            
    if os.path.exists( os.path.join(SRC, "2025") ):
        shutil.rmtree( os.path.join(SRC, "2025") )
        logger.info(f"Deleted existing folder: {os.path.join(SRC, '2025')}")

    #imageSorting()
    IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png')
    VIDEO_EXTENSIONS = ('.mp4', '.mkv', '.mov', '.avi', '.m4a', '.webm')
    SUPPORTED_EXTENSIONS = IMAGE_EXTENSIONS + VIDEO_EXTENSIONS

    for filename in os.listdir(SRC):
        if not filename.lower().endswith(SUPPORTED_EXTENSIONS):
            continue

        full_path = os.path.join(SRC, filename)
        creation_date = get_file_creation_date(full_path)

        if creation_date:
            destination_folder = build_destination_path(SRC, creation_date)
            copy_and_move_to_raw(full_path, destination_folder)
        else:
            logger.info(f"Skipped (no date found): {filename}")

    #monthOrganizer()
    dst=os.path.join(SRC, "2025")
    organize_folders_by_month(dst)

    dst=os.path.join(SRC, "2024")
    organize_folders_by_month(dst)

def photograph_edits():

    SRC = r"E:\Phone Backups\Photography Edits"
    DST = r"E:\Images\Photography Edits"

    if os.path.exists( os.path.join(DST, "2024") ):
        shutil.rmtree( os.path.join(DST, "2024") )
        logger.info(f"Deleted existing folder: {os.path.join(DST, '2024')}")
            
    if os.path.exists( os.path.join(DST, "2025") ):
        shutil.rmtree( os.path.join(DST, "2025") )
        logger.info(f"Deleted existing folder: {os.path.join(DST, '2025')}")

    # Copy the backup
    if os.path.isdir(SRC):
        os.makedirs(DST, exist_ok=True)
        for item in os.listdir(SRC):
            src_item = os.path.join(SRC, item)
            dst_item = os.path.join(DST, item)
            if os.path.isdir(src_item):
                shutil.copytree(src_item, dst_item, dirs_exist_ok=True)
            else:
                shutil.copy2(src_item, dst_item)
                logger.info(f"Copied file: {src_item} to {dst_item}")
        logger.info("Snapchat copied successfully.")
    else:
        logger.info(f"Source folder not found: {SRC}")

    #imageSorting()
    IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png')
    VIDEO_EXTENSIONS = ('.mp4', '.mkv', '.mov', '.avi', '.m4a', '.webm')
    SUPPORTED_EXTENSIONS = IMAGE_EXTENSIONS + VIDEO_EXTENSIONS

    
    for filename in os.listdir(DST):
        if not filename.lower().endswith(SUPPORTED_EXTENSIONS):
            continue

        full_path = os.path.join(DST, filename)
        creation_date = get_file_creation_date(full_path)

        if creation_date:
            destination_folder = build_destination_path(DST, creation_date)
            copy_and_move_to_raw(full_path, destination_folder)
        else:
            logger.info(f"Skipped (no date found): {filename}")

    #monthOrganizer()
    dst=os.path.join(DST, "2025")
    organize_folders_by_month(dst)

    dst=os.path.join(DST, "2024")
    organize_folders_by_month(dst)

if __name__ == "__main__":
    logger=app_loggerSetup()
    logger.info("App started")
    
    snapchat()
    whatsapp()
    whatsapp_SENT()
    photograph_edits()