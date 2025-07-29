import logging
import tkinter as tk # Import tkinter for the GUI root window

# Import the AppVariables class for centralized configuration

from scripts.variables import AppVariables

# Import your GUI application class from gui_app.py
from gui_app import RenamerApp

# Import loggerSetup from your scripts.functions module
# This function is responsible for setting up the logging handlers and formatters.
from scripts.functions import loggerSetup

# Initialize the logger for this main module.
# Log messages from this logger will also go to the GUI's log window
# once loggerSetup configures the root logger.
logger = logging.getLogger(__name__)

def main():
    """
    Main function to initialize the logging system and launch the Tkinter GUI application.
    This file now acts purely as the entry point for the GUI.
    """
    # 1. Configure the logging system first.
    # This ensures that all subsequent log messages (from GUI or core functions)
    # are captured by the file handler and the GUI's TextWidgetHandler.
    loggerSetup(
        log_file_name=AppVariables.LOG_FILE_NAME,
        log_level=AppVariables.LOG_LEVEL,
        file_mode=AppVariables.LOG_FILE_MODE
    )
    logger.info("Application starting up: Initializing GUI.")

    # 2. Create the main Tkinter root window.
    # This is the top-level window for your GUI application.
    root = tk.Tk()
    root.title("Media Renamer Application") # Set the title of the main window

    # 3. Create an instance of your RenamerApp GUI class.
    # This will build all the user interface elements within the 'root' window.
    app = RenamerApp(root)

    # 4. Start the Tkinter event loop.
    # This line is crucial for a GUI application. It makes the window appear,
    # keeps it responsive to user interactions (clicks, keyboard input),
    # and processes all Tkinter events. The script will remain running
    # until the window is closed.
    root.mainloop()

    logger.info("Application closed: GUI window terminated.")

# Entry point for the script execution.
# This block ensures that 'main()' is called only when the script is executed directly.
if __name__ == "__main__":
    main()
