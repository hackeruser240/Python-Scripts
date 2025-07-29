import tkinter as tk
from tkinter import filedialog, messagebox
import logging
import os
import sys
import pandas as pd

# Import AppVariables for centralized configuration
from scripts.variables import AppVariables

# Import core functions for renaming logic
# Ensure 'scripts' is a package (i.e., has an __init__.py file)
# or adjust the import path if functions.py is directly in the same directory.
from scripts.functions import (
    findMedia,
    renamingStrings,
    renamingFiles,
    loggerSetup # loggerSetup is called in renamingMedia.py, but good to know it's there
)

# --- Custom Logging Handler for Tkinter Text Widget ---
class TextWidgetHandler(logging.Handler):
    """
    A custom logging handler that sends log records to a Tkinter Text widget.
    """
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
        self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    def emit(self, record):
        """
        Emit a record.
        Appends the formatted log message to the Tkinter Text widget.
        """
        msg = self.format(record)
        # Use after() to ensure the message is added on the main Tkinter thread
        self.text_widget.after(0, self.append_message, msg)

    def append_message(self, msg):
        """
        Appends the message to the text widget and scrolls to the end.
        """
        self.text_widget.configure(state='normal') # Enable editing
        self.text_widget.insert(tk.END, msg + '\n')
        self.text_widget.see(tk.END) # Scroll to the end
        self.text_widget.configure(state='disabled') # Disable editing


# --- Main Tkinter Application Class ---
class RenamerApp:
    """
    Tkinter GUI application for renaming media files.
    """
    def __init__(self, master):
        """
        Initializes the RenamerApp GUI.

        Args:
            master: The root Tkinter window (tk.Tk instance).
        """
        self.master = master
        master.title("Media Renamer")
        master.geometry("700x600") # Set a default window size
        master.resizable(True, True) # Allow window resizing

        # Configure grid weights for responsive layout
        master.grid_rowconfigure(0, weight=0) # Controls frame
        master.grid_rowconfigure(1, weight=1) # Log window
        master.grid_columnconfigure(0, weight=1)

        # --- Variables ---
        self.directory_path = tk.StringVar()
        self.media_type = tk.StringVar(value=AppVariables.MEDIA_TYPE_IMAGES) # Default to images

        # --- Frames for layout ---
        self.controls_frame = tk.Frame(master, padx=10, pady=10)
        self.controls_frame.grid(row=0, column=0, sticky="nsew")
        self.controls_frame.grid_columnconfigure(1, weight=1) # Make entry field expandable

        self.log_frame = tk.Frame(master, padx=10, pady=10)
        self.log_frame.grid(row=1, column=0, sticky="nsew")
        self.log_frame.grid_rowconfigure(0, weight=1)
        self.log_frame.grid_columnconfigure(0, weight=1)


        # --- 1. Directory Browse Field ---
        tk.Label(self.controls_frame, text="Directory:").grid(row=0, column=0, sticky="w", pady=5)
        self.directory_entry = tk.Entry(self.controls_frame, textvariable=self.directory_path, width=50)
        self.directory_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.browse_button = tk.Button(self.controls_frame, text="Browse", command=self.browse_directory)
        self.browse_button.grid(row=0, column=2, sticky="e", padx=5, pady=5)

        # --- 2. "Media" Selection ---
        tk.Label(self.controls_frame, text="Media Type:").grid(row=1, column=0, sticky="w", pady=5)
        self.image_radio = tk.Radiobutton(self.controls_frame, text="Images", variable=self.media_type, value=AppVariables.MEDIA_TYPE_IMAGES)
        self.image_radio.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        self.video_radio = tk.Radiobutton(self.controls_frame, text="Videos", variable=self.media_type, value=AppVariables.MEDIA_TYPE_VIDEOS)
        self.video_radio.grid(row=1, column=1, sticky="w", padx=(80,0), pady=5) # Offset to place next to images radio

        # --- Action Button ---
        self.rename_button = tk.Button(self.controls_frame, text="Start Renaming", command=self.start_renaming,
                                       font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                                       activebackground="#45a049", activeforeground="white", relief=tk.RAISED, bd=3)
        self.rename_button.grid(row=2, column=0, columnspan=3, pady=15)


        # --- 3. Log Window ---
        tk.Label(self.log_frame, text="Log Output:").grid(row=0, column=0, sticky="w")
        self.log_text_widget = tk.Text(self.log_frame, wrap='word', state='disabled', bg="#f0f0f0", fg="black", font=("Courier New", 10))
        self.log_text_widget.grid(row=1, column=0, sticky="nsew", pady=5)

        self.log_scrollbar = tk.Scrollbar(self.log_frame, command=self.log_text_widget.yview)
        self.log_scrollbar.grid(row=1, column=1, sticky="ns")
        self.log_text_widget.config(yscrollcommand=self.log_scrollbar.set)

        # Attach custom handler to the root logger
        self.log_handler = TextWidgetHandler(self.log_text_widget)
        logging.getLogger().addHandler(self.log_handler) # Add to root logger
        logging.getLogger().setLevel(AppVariables.LOG_LEVEL) # Ensure root logger level is set

        # Initial log message to confirm setup
        logging.info("GUI application initialized. Please select a directory and media type.")


    def browse_directory(self):
        """
        Opens a directory selection dialog and updates the directory path entry.
        """
        selected_directory = filedialog.askdirectory()
        if selected_directory:
            self.directory_path.set(selected_directory)
            logging.info(f"Selected directory: {selected_directory}")
        else:
            logging.warning("Directory selection cancelled.")

    def start_renaming(self):
        """
        Initiates the media renaming process based on user inputs.
        This function calls the core logic from scripts.functions.
        """
        path = self.directory_path.get()
        media = self.media_type.get()

        if not path:
            messagebox.showerror("Input Error", "Please select a directory first.")
            logging.error("Renaming aborted: No directory selected.")
            return

        if not os.path.isdir(path):
            messagebox.showerror("Input Error", f"The selected path '{path}' is not a valid directory.")
            logging.error(f"Renaming aborted: Invalid directory path '{path}'.")
            return

        logging.info(f"Starting renaming process for path: '{path}' and media type: '{media}'")

        try:
            # 1. Find and categorize media files
            numbers_df, strings_df = findMedia(media, path)
            logging.info("Initial media categorization complete.")
            logging.info(f"Found {len(numbers_df)} numeric files and {len(strings_df)} string files.")

            max_existing_number = 0

            # 2. Process numeric files
            if not numbers_df.empty:
                numbers_df = numbers_df.sort_values(by='Filenames', ascending=True, ignore_index=True)
                existing_numeric_names_set = set(numbers_df['Filenames'].tolist())
                new_names_for_numbers = []
                current_expected_number = 1

                for index, row in numbers_df.iterrows():
                    if row['Filenames'] == current_expected_number:
                        new_names_for_numbers.append(current_expected_number)
                        current_expected_number += 1
                    else:
                        while current_expected_number in existing_numeric_names_set:
                            current_expected_number += 1
                        new_names_for_numbers.append(current_expected_number)
                        current_expected_number += 1
                numbers_df['New names'] = new_names_for_numbers
                max_existing_number = numbers_df['New names'].max()
                logging.info("Numeric files processed for new names.")
            else:
                logging.info("No numeric filenames found in the given path.")
                max_existing_number = 0

            # 3. Determine starting point for string files
            starting_point_for_strings = max_existing_number + 1
            logging.info(f"Starting point for renaming string files: {starting_point_for_strings}")

            # 4. Process string files
            if not strings_df.empty:
                strings_df = renamingStrings(strings_df, starting_point_for_strings)
                logging.info("String files processed for new names.")
            else:
                logging.info("Not processing any string names.")

            # 5. Combine both DataFrames
            final_df = pd.DataFrame() # Ensure pd is imported
            if numbers_df.empty and strings_df.empty:
                logging.info("No media files found to rename.")
            elif numbers_df.empty:
                final_df = strings_df
            elif strings_df.empty:
                final_df = numbers_df
            else:
                final_df = pd.concat([numbers_df, strings_df], ignore_index=True)
                final_df['New names'] = final_df['New names'].astype("Int64")

            # Sort final DataFrame by 'New names'
            if not final_df.empty:
                final_df = final_df.sort_values(by='New names', ascending=True, ignore_index=True)
            
            logging.info("\n--- Final Renaming Plan ---")
            if not final_df.empty:
                logging.info(final_df.to_string())
            else:
                logging.info("No files to rename based on the final plan.")

            # 6. Finally rename the files
            if not final_df.empty:
                renamingFiles(final_df, path)
                messagebox.showinfo("Success", "Media renaming process completed!")
                logging.info("Media renaming process completed successfully.")
            else:
                messagebox.showinfo("Info", "No files were found or needed renaming.")
                logging.info("No files were found or needed renaming.")

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            logging.exception("An unexpected error occurred during renaming process.") # Logs traceback

