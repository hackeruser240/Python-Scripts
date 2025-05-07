'''
08-May-2025: Thursday
This code was developed as an enhanced functionality of the main YelpDataExtractor script. For an updated version, go there. This has become obselete. 
'''
import os
import shutil
import argparse
import pandas as pd


def get_folder_names(base_path):
    return [
        name for name in os.listdir(base_path)
        if os.path.isdir(os.path.join(base_path, name))
    ]


def process_csv(name, folder_path, base_path):
    service_name = os.path.basename(base_path)
    target_file = f"{service_name}_multiple_PCs_AD.csv"
    file_path = os.path.join(folder_path, target_file)

    if not os.path.exists(file_path):
        print(f"⚠️ File not found: {file_path}")
        return

    df = pd.read_csv(file_path)
    df_cleaned = df.drop_duplicates(subset='Phone Numbers', keep='first')
    df_cleaned.reset_index(drop=True, inplace=True)

    #Extracting the last name
    
    folder_name = os.path.basename(base_path)
    cleaned_folder = os.path.join(base_path, f'Cleaned {folder_name}')
    os.makedirs(cleaned_folder, exist_ok=True)

    output_file = os.path.join(cleaned_folder, f"{name}.csv")
    df_cleaned.to_csv(output_file, index=False)

    print(f"✅ Cleaned and saved: {name}")


def find_missing_ad_files(folder_names, base_path):
    missing_folders = []

    for name in folder_names:
        folder_path = os.path.join(base_path, name)

        has_ad_csv = any(
            f.endswith('_AD.csv') for f in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, f))
        )

        if has_ad_csv:
            process_csv(name, folder_path, base_path)
        else:
            print(f"🚫 Missing _AD.csv file in: {name}")
            missing_folders.append(name)

    return missing_folders


def move_folders_except_cleaned(base_path):
    folder_name = os.path.basename(base_path)
    #cleaned_folder = os.path.join(base_path, 'Cleaned')
    cleaned_folder = os.path.join(base_path, f'Cleaned {folder_name}')
    other_folder = os.path.join(base_path, 'Other')

    if not os.path.exists(cleaned_folder):
        print("❌ Error: 'Cleaned' folder does not exist in the base path.")
        return

    os.makedirs(other_folder, exist_ok=True)

    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)

        if os.path.isdir(item_path) and item not in [f'Cleaned {folder_name}', 'Other']:
            shutil.move(item_path, os.path.join(other_folder, item))
            print(f"📦 Moved '{item}' to 'Other'")

    print(f"\n🎉 All folders (except 'Cleaned {folder_name}' and 'Other') moved.")


def removingDuplications(base_path):
    folder_names = get_folder_names(base_path)
    missing_folders = find_missing_ad_files(folder_names, base_path)

    if missing_folders:
        print("\n📌 Folders missing _AD.csv:")
        for folder in missing_folders:
            print(f" - {folder}")

    move_folders_except_cleaned(base_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', help='Add your path')
    args = parser.parse_args()

    removingDuplications(args.path)