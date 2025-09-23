from main import combined,custom_folder_make
from tkinter import messagebox
import tkinter as tk

def on_button_click():
    dst_path=custom_folder_make(
        folder_name=folder_name.get()
    )

    combined(
        template_path = template_entry.get(),
        dst_path=dst_path
    )

    messagebox.showinfo("Folder Created", f'"{folder_name.get()}" has been created!')


# Create main window
root = tk.Tk()
root.title("CV Template Deployer")
root.geometry("500x500")

# Label
label = tk.Label(root, text="Template Path:")
label.pack(pady=(20, 0))
# Entry with default value
default_path = r"D:\My Documents [D-drive]\latex_tempate_for_CV.rar"
template_entry = tk.Entry(root, width=70)
template_entry.insert(0, default_path)
template_entry.pack(pady=5)

#By default job folder name
label=tk.Label(root,text="Job Folder Directory")
label.pack(pady=(20,0))
default_job_folder=r"D:\My Documents [D-drive]\Job Applications\2025"
job_folder=tk.Entry(root, width=70)
job_folder.insert(0, default_job_folder)
job_folder.pack(pady=5)


label=tk.Label(root,text="Folder/Company Name:")
label.pack(pady=(20,0))
folder_name=tk.Entry(root,width=70)
folder_name.pack(pady=5)
# Add a button
button = tk.Button(root, text="Process", command=on_button_click)
button.pack(pady=20)

# Start the GUI loop
root.mainloop()