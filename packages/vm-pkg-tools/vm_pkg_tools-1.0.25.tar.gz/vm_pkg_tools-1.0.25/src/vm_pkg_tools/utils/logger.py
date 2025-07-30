import logging
import os
from colorlog import ColoredFormatter


def setup_logging(
    log_file_path="output/logs/processing.log",
    file_level=logging.DEBUG,  # DEBUG logs will go to the file
    console_level=logging.INFO,  # INFO (or higher) logs will show in the terminal
    log_format="%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]",
):
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    # Clear existing handlers
    root_logger = logging.getLogger()
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # File handler (detailed logs)
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_handler.setLevel(file_level)
    file_handler.setFormatter(logging.Formatter(log_format))

    # Console handler (minimal logs)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    color_formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )
    console_handler.setFormatter(color_formatter)

    # Add handlers
    logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, console_handler])
