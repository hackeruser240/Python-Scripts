import os
import subprocess
import time
from tqdm import tqdm

BASE_DIR = r"E:\Images\0\EME College"

def list_folders(directory):
    return [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]

def get_folder_size(folder_path):
    total_size = 0
    for dirpath, _, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total_size += os.path.getsize(fp)
    return total_size

def simulate_progress(size_bytes):
    steps = 50
    delay = max(0.05, min(0.5, size_bytes / (1024**3)))  # Delay based on GB size
    for _ in tqdm(range(steps), desc="Compressing", unit="step"):
        time.sleep(delay / steps)

def compress_with_rar5(folder_path, output_path):
    command = [r"C:\Program Files\WinRAR\WinRAR.exe", "a", "-ma5", "-r", f"{output_path}.rar", folder_path]
    subprocess.run(command, check=True)

def compress_with_7z(folder_path, output_path):
    command = [r"C:\Program Files\7-Zip\7z.exe", "a", "-t7z", f"{output_path}.7z", folder_path]
    subprocess.run(command, check=True)

def compress_folder(folder_name, method):
    folder_path = os.path.join(BASE_DIR, folder_name)
    output_path = os.path.join(BASE_DIR, folder_name)
    size = get_folder_size(folder_path)
    simulate_progress(size)

    if method == "rar5":
        compress_with_rar5(folder_path, output_path)
    elif method == "7z":
        compress_with_7z(folder_path, output_path)
    else:
        raise ValueError("Unsupported compression method")

if __name__ == "__main__":
    print("Choose compression method:")
    print("1. RAR5")
    print("2. 7z")
    choice = input("Enter 1 or 2: ").strip()

    method = "rar5" if choice == "1" else "7z" if choice == "2" else None
    if not method:
        print("Invalid choice. Exiting.")
        exit(1)

    folders = list_folders(BASE_DIR)
    print(f"Found {len(folders)} folders to compress using {method.upper()}...")

    for folder in folders:
        print(f"\n📁 Compressing: {folder}")
        try:
            compress_folder(folder, method)
            print(f"✅ {folder} compressed successfully.")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to compress {folder}.")