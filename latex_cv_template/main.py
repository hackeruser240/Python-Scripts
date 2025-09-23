# filename: latex_cv_template.py

import shutil
import rarfile
import os
from datetime import datetime

def copy_template(src_path,dst_path):
    if src_path and dst_path:
        shutil.copy2(src_path, dst_path)  # preserves metadata
        print("file copied")
    else:
        print("some error")

def unzip_to(template_path,dst_path):
    #rar_path = r"D:\My Documents\CV.rar"
    rarfile.UNRAR_TOOL = r"C:\Program Files\WinRAR\UnRAR.exe"
    
    with rarfile.RarFile(template_path) as rf:
        rf.extractall(path=dst_path)

    print(f"✅ Extracted to: {dst_path}")

def delete_rarfile(path):
    path=os.path.join(path,"latex_tempate_for_CV.rar")
    if os.path.exists(path):
        os.remove(path)
        print(f"🗑️ Deleted: {path}")
    else:
        print(f"⚠️ File not found: {path}")

def custom_folder_make(folder_name):
    dst_path=r"D:\My Documents [D-drive]\Job Applications\2025"
    #dst_path=os.path.join(dst_path,folder_name)
    
    today = datetime.today()
    formatted_date = today.strftime("%d-%b-%Y")
    folder_name=f"{folder_name} {formatted_date}"

    dst_path=os.path.join(dst_path,folder_name)

    os.makedirs(dst_path,exist_ok=True)

    return dst_path

def combined(template_path,dst_path):
    copy_template(src_path=template_path, dst_path=dst_path)
    unzip_to(template_path=template_path,dst_path=dst_path)
    delete_rarfile(dst_path)

if __name__ == "__main__":
    template_path=r"D:\My Documents [D-drive]\latex_tempate_for_CV.rar"
    dst_path=r"D:\My Documents [D-drive]\Job Applications\2025\test_dir123"
    os.makedirs(dst_path,exist_ok=True)

    folder_name=input(f"enter name of folder/company to create:")
    if folder_name:
        dst_path=custom_folder_make(folder_name=folder_name)

    combined(template_path=template_path,dst_path=dst_path)