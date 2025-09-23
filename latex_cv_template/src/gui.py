import os
from main import combined,custom_folder_make
from tkinter import messagebox
import tkinter as tk

def on_button_click():
    button.config(state="disabled")

    try:
        # Get user inputs
        folder = folder_name.get().strip()
        template = template_entry.get().strip()
        job_dir = job_folder.get().strip()

        # Validate inputs
        if not folder:
            messagebox.showerror("Input Error", "Folder/Company name is required.")
            return
        if not os.path.exists(template):
            messagebox.showerror("File Error", f"Template file not found:\n{template}")
            return
        if not os.path.exists(job_dir):
            messagebox.showerror("Directory Error", f"Job folder path does not exist:\n{job_dir}")
            return

        # Create folder and deploy template
        dst_path = custom_folder_make(folder_name=folder)
        combined(template_path=template, dst_path=dst_path)

        # Success message
        messagebox.showinfo("Success", f'"{folder}" has been created successfully!')

    except Exception as e:
        messagebox.showerror("Unexpected Error", f"Something went wrong while executing GUI:\n{str(e)}")

    finally:
        button.config(state="normal")

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