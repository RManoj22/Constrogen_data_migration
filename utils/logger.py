import logging
import logging.config

# Optional: Set up logging configuration (you can also do this in a config file)
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
LOG_LEVEL = logging.DEBUG

# Create a custom logger
logger = logging.getLogger("app_logger")

# Set the log level
logger.setLevel(LOG_LEVEL)

# Create handlers
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("app.log")

# Set level for handlers
console_handler.setLevel(LOG_LEVEL)
file_handler.setLevel(logging.INFO)

# Create formatters and add it to handlers
formatter = logging.Formatter(LOG_FORMAT)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
