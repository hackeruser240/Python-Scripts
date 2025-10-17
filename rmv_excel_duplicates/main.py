import csv
from collections import defaultdict
import shutil
import os
import logging

def logger_Setup():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('email_deduplication.log')
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%Y %I:%M %p')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

def remove_duplicates(input_file):
    # Read all email rows (no header expected)
    with open(input_file, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        email_rows = [row[0].strip() for row in reader if row]

    seen = set()
    duplicates = defaultdict(list)
    deduplicated_rows = []

    for email in email_rows:
        if email not in seen:
            seen.add(email)
            deduplicated_rows.append([email])
        else:
            duplicates[email].append(email)

    # Display duplicates
    if duplicates:
        logger.info("Duplicate emails found (excluding first occurrence):")
        for email, entries in duplicates.items():
            logger.info(f"{email} ({len(entries)} duplicates)")
    else:
        logger.info("No duplicates found.")

    # Save deduplicated emails to new file
    output_file = input_file.replace('.csv', '_deduplicated.csv')
    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(deduplicated_rows)

    logger.info(f"Deduplicated file saved as: {output_file}")

def sort_emails_by_local_part(output_file):
    # Read deduplicated emails
    with open(output_file, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        email_rows = [row[0].strip() for row in reader if row]

    # Sort by local part (before '@')
    sorted_rows = sorted(email_rows, key=lambda email: email.split('@')[0])

    # Overwrite the file with sorted emails
    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for email in sorted_rows:
            writer.writerow([email])

    logger.info(f"Sorted emails saved in: {output_file}")

def remove_emails_by_domain_suffix(input_file, suffix_list_file):
    # Load domain suffixes
    with open(suffix_list_file, mode='r', encoding='utf-8') as f:
        suffixes = [line.strip().lower() for line in f if line.strip()]

    # Read original email list
    with open(input_file, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        email_rows = [row[0].strip() for row in reader if row]

    # Filter out emails matching any suffix
    filtered_rows = []
    count=0
    for email in email_rows:
        domain = email.split('@')[-1].lower()
        if not any(domain.endswith(suffix) for suffix in suffixes):
            filtered_rows.append([email])
        else:
            logger.info(f"Removed email: {email}")
            count += 1

    # Save to a new file
    output_file = input_file.replace('.csv', '_domain_filtered.csv')
    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(filtered_rows)

    logger.info(f"Total emails removed based on domain suffixes: {count}")
    logger.info(f"Domain-filtered file saved as: {output_file}")

if __name__ == "__main__":
    logger=logger_Setup()
    source = os.path.expanduser(r"C:\Users\HP\Downloads\emails.csv")
    destination = r"C:\Users\HP\OneDrive\Documents\pythonScripts\Py_scripts\rmv_excel_duplicates\emails.csv"

    # Copy and overwrite
    shutil.copy2(source, destination)
    logger.info(f"Copied and overwritten: {destination}")

    input_file = r"emails.csv"
    dedup_file = input_file.replace('.csv', '_deduplicated.csv')
    suffix_list_file = r"temp emails list.txt"

    remove_duplicates(input_file)
    sort_emails_by_local_part(dedup_file)
    remove_emails_by_domain_suffix(dedup_file, suffix_list_file)