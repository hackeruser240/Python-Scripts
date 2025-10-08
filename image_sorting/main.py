import shutil, os
from functions.imageSorting import *
from functions.monthOrganizer import organize_folders_by_month

def snapchat():
    SRC = r"E:\Phone Backups\Snapchat"
    DST = r"E:\Images\Snapchat"

    if os.path.exists( os.path.join(DST, "2024") ):
        shutil.rmtree( os.path.join(DST, "2024") )
        print(f"Deleted existing folder: {os.path.join(DST, '2024')}")
            
    if os.path.exists( os.path.join(DST, "2025") ):
        shutil.rmtree( os.path.join(DST, "2025") )
        print(f"Deleted existing folder: {os.path.join(DST, '2025')}")

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
                print(f"Copied file: {src_item} to {dst_item}")
        print("Snapchat copied successfully.")
    else:
        print(f"Source folder not found: {SRC}")

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
            print(f"Skipped (no date found): {filename}")

    #monthOrganizer()
    DST=os.path.join(DST, "2025")
    organize_folders_by_month(DST)
    DST=os.path.join(DST, "2024")
    organize_folders_by_month(DST)

if __name__ == "__main__":
    snapchat()