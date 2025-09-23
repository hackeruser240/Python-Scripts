# filename: latex_cv_template.py

import shutil
import rarfile
import os
from datetime import datetime

def copy_template(src_path, dst_path):
    try:
        if not os.path.exists(src_path):
            raise FileNotFoundError(f"Template not found at: {src_path}")
        shutil.copy2(src_path, dst_path)
        print("✅ Template copied successfully.")
    except Exception as e:
        print(f"❌ Failed to copy template: {e}")

def unzip_to(template_path, dst_path):
    try:
        rarfile.UNRAR_TOOL = r"C:\Program Files\WinRAR\UnRAR.exe"
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"RAR file not found at: {template_path}")
        with rarfile.RarFile(template_path) as rf:
            rf.extractall(path=dst_path)
        print(f"✅ Extracted to: {dst_path}")
    except rarfile.Error as e:
        print(f"❌ RAR extraction error: {e}")
    except Exception as e:
        print(f"❌ Failed to unzip template: {e}")

def delete_rarfile(path):
    try:
        rar_path = os.path.join(path, "latex_tempate_for_CV.rar")
        if os.path.exists(rar_path):
            os.remove(rar_path)
            print(f"🗑️ Deleted: {rar_path}")
        else:
            print(f"⚠️ File not found: {rar_path}")
    except Exception as e:
        print(f"❌ Failed to delete RAR file: {e}")

def custom_folder_make(folder_name):
    try:
        base_path = r"D:\My Documents [D-drive]\Job Applications\2025"
        today = datetime.today()
        formatted_date = today.strftime("%d-%b-%Y")
        final_folder_name = f"{folder_name} {formatted_date}"
        dst_path = os.path.join(base_path, final_folder_name)
        os.makedirs(dst_path, exist_ok=True)
        print(f"📁 Folder created: {dst_path}")
        return dst_path
    except Exception as e:
        print(f"❌ Failed to create folder: {e}")
        return None

def combined(template_path, dst_path):
    if not dst_path:
        print("⚠️ Destination path is invalid. Skipping operations.")
        return
    copy_template(src_path=template_path, dst_path=dst_path)
    unzip_to(template_path=template_path, dst_path=dst_path)
    delete_rarfile(dst_path)


if __name__ == "__main__":
    template_path=r"D:\My Documents [D-drive]\latex_tempate_for_CV.rar"
    
    if True:
        dst_path=r"D:\My Documents [D-drive]\Job Applications\2025\test_dir123"
        os.makedirs(dst_path,exist_ok=True)
    else:
        folder_name=input(f"enter name of folder/company to create:")
        if folder_name:
            dst_path=custom_folder_make(folder_name=folder_name)

    combined(template_path=template_path,dst_path=dst_path)