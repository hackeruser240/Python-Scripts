import os
import shutil

def find_pdfs(directory):
    pdf_files = []  # List to store PDF file paths

    # Walk through the directory tree
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))

    return pdf_files

# Specify the directory to search for PDF files
directory_to_search = 'C:/Users/HP/Dropbox/PTUT/Teaching/Spring 2024/Teaching/Courses/Data & Computer Comm/Lab'

# Call the function to find PDF files
pdfs = find_pdfs(directory_to_search)

# Print the paths of the PDF files found
for pdf in pdfs:
    print(pdf)
    
    
def extract_and_copy_pdfs(source_directory, destination_directory):
    pdf_files = []
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            if file.endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    
    for pdf_file in pdf_files:
        shutil.copy(pdf_file, destination_directory)

# Example usage:
source_directory_path = 'C:/Users/HP/Dropbox/PTUT/Teaching/Spring 2024/Teaching/Courses/Data & Computer Comm/Lab'
destination_directory_path = 'C:/Users/HP/Dropbox/PTUT/Teaching/Spring 2024/Teaching/Courses/Data & Computer Comm/Lab/'
extract_and_copy_pdfs(source_directory_path, destination_directory_path)