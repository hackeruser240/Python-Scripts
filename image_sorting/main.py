import shutil, os

if __name__ == "__main__":
    SRC = r"E:\Phone Backups\Snapchat"
    DST = r"E:\Images\Snapchat"

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