# Media Renamer Application

This repository contains a Python application designed to help you organize your media files (images and videos) by renaming them into a sequential numerical order. It provides a user-friendly Graphical User Interface (GUI) built with `tkinter`.

## 1. Purpose of the Script

The primary purpose of this script is to bring order to disarranged media collections. It scans a specified directory, identifies image and video files, and then renames them sequentially. Numeric files are renumbered to fill any gaps and ensure continuity, while string-named files are assigned new sequential numbers starting from the next available number after the existing numeric files.

## 2. How to Run It

You can run this application either directly from Python source files or as a standalone executable (after building it with PyInstaller).

### Running from Source

1.  **Prerequisites:**
    * Python 3.x installed.
    * `pandas` library: `pip install pandas`
    * `tkinter` (usually comes with Python, but ensure it's available).

2.  **Clone the Repository (or download the files):**
    ```bash
    git clone <repository_url>
    cd <repository_name> # Navigate to the root directory where renamingMedia.py is located
    ```

3.  **Ensure correct directory structure:**
    Your project structure should look like this:
    ```
    .
    ├── renamingMedia.py
    ├── gui_app.py
    ├── assets/
    │   ├── app_icon.png  (or .ico if you changed the config)
    ├── scripts/
    │   ├── __init__.py  (empty file to make 'scripts' a Python package)
    │   ├── functions.py
    │   └── variables.py
    ├── requirements.bat
    └── build.bat (if you created it)
    ```

4.  **Execute the main script:**
    From your terminal in the project root directory:
    ```bash
    python renamingMedia.py
    ```
    This will launch the GUI application.

### Running as a Standalone Executable

If you have built the application into an executable (see "How to Install It" below), navigate to the `dist` folder created by PyInstaller and double-click the `Renaming Media.exe` file.

## 3. How to Install It (Building the Executable)

To create a standalone executable that doesn't require a Python environment on the target machine, you can use `PyInstaller`.

1.  **Prerequisites:**
    * Python 3.x installed.
    * `PyInstaller` library: `pip install pyinstaller`
    * `pandas` library: `pip install pandas` (needed for the build process)

2.  **Create Virtual Environment (recommended)**
    Activate your python terminal.
   

3.  **Run `requirements.bat`**
    To make sure your python environment has the required modules, you may run the `requirements.bat` to install/update the necessary packages.

4.  **Using `build.bat` (Recommended):**
    If you have the `build.bat` file from the instructions, just run:
    ```bash
    build.bat
    ```
    This batch file automates cleaning previous builds and then running PyInstaller. This command is bundled into a single executable file (`--onefile`), cleans previous build artifacts, names the executable "Renaming Media", and includes necessary data files.

    ```bash
    pyinstaller --clean --onefile --noconsole --name="Renaming Media" ^
    --add-data "app_icon.png;." ^
    renamingMedia.py
    ```
    * `--clean`: Cleans PyInstaller cache and removes temporary files.
    * `--onefile`: Packages the application into a single executable file.
    * `--noconsole`: Prevents a console window from opening when the GUI app is launched.
    * `--name="Renaming Media"`: Sets the name of the executable file to `Renaming Media.exe`.
    * `--add-data "app_icon.png;."`: **Crucially**, this tells PyInstaller to include `app_icon.png` (the source file, relative to your current directory) into the root of the executable's temporary extraction folder (`.`). This is essential for the GUI to find and display the icon.
    * `renamingMedia.py`: The main script file to start the application.

5.  **Find the Executable:**
    After a successful build, a `dist` folder will be created in your project directory. Inside `dist`, you will find `Renaming Media.exe`. This is your standalone application.

## 4. Brief Description of Each File

* **`renamingMedia.py`**:
    * This is the **main entry point** of the application.
    * Its primary role is to set up the logging system, initialize the `tkinter` root window, create an instance of the `RenamerApp` (your GUI), and start the `tkinter` event loop. It acts as the bridge between your system and the GUI application.

* **`gui_app.py`**:
    * This file contains the **Graphical User Interface (GUI) logic** of the application.
    * It defines the `RenamerApp` class, which handles the creation of all GUI widgets (buttons, text fields, radio buttons, log window), manages user interactions (e.g., Browse directories, starting the renaming process), and calls the core renaming functions from `scripts/functions.py`.
    * It also includes `TextWidgetHandler` to redirect `logging` output to the GUI's log display.

* **`scripts/functions.py`**:
    * This file contains the **core business logic** for media renaming.
    * It defines functions like `findMedia` (to identify and categorize media files), `renamingStrings` (to assign new names to string-based files), `renamingFiles` (to perform the actual file system renaming operations), and `loggerSetup` (for configuring the logging system). These functions are agnostic to the GUI and could theoretically be used in a command-line interface as well.

* **`scripts/variables.py`**:
    * This file defines the `AppVariables` class, which serves as a **centralized repository for application-wide configuration variables and constants**.
    * It includes definitions for media types (`MEDIA_TYPE_IMAGES`, `MEDIA_TYPE_VIDEOS`), supported file extensions (`IMAGE_EXTENSIONS`, `VIDEO_EXTENSIONS`), and logging configurations (`LOG_FILE_NAME`, `LOG_LEVEL`, `LOG_FILE_MODE`). This approach helps in managing and easily modifying application settings from a single location.

* **`app_icon.png`**:
    * This is the **application icon file**. It is used by `gui_app.py` to set the icon for the Tkinter window and by PyInstaller to potentially set the icon for the generated executable file itself. (Note: `.png` is generally preferred for `tkinter.PhotoImage` and `iconphoto` for better cross-platform compatibility with bundled apps).

* **`build.bat`**:
    * A Windows batch script that automates the process of cleaning previous `build` and `dist` folders and then running the `PyInstaller` command with all necessary flags to create the executable.