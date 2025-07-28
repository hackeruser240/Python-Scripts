import logging

class AppVariables:
    """
    A class to hold application-wide configuration variables and constants.
    """

    # --- Media Type Definitions ---
    MEDIA_TYPE_IMAGES = 'images'
    MEDIA_TYPE_VIDEOS = 'videos'

    # --- Supported File Extensions ---
    IMAGE_EXTENSIONS = ('.JPG', '.JPEG', '.PNG', '.GIF', '.BMP', '.TIFF', '.JFIF')
    VIDEO_EXTENSIONS = ('.mp4', '.mpeg', '.mkv', '.avi', '.mov', '.wmv', '.flv')

    # --- Logging Configuration ---
    LOG_FILE_NAME = "log.txt"
    LOG_LEVEL = logging.INFO  # Default logging level
    LOG_FILE_MODE = 'w'       # Default file mode for log file ('w' for overwrite, 'a' for append)

    # You can add more variables here as your application grows, e.g.,
    # DEFAULT_DIRECTORY = os.getcwd() # Example for a default directory