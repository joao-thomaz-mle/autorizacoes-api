import json
import logging

from app.utils.config import load_config

config = load_config()


class ColoredJSONFormatter(logging.Formatter):
    # ANSI color codes
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[31m",  # Red
        "ERROR": "\033[91m",  # Bright Red
        "CRITICAL": "\033[95m",  # Magenta
        "RESET": "\033[0m",  # Reset color
    }

    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            "filename": record.filename,
            "lineno": record.lineno,
        }

        # Get the color for the log level
        color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        reset = self.COLORS["RESET"]

        # Format JSON with highlighted message
        json_output = json.dumps(log_record, ensure_ascii=False)

        # Highlight the message content with bold and brighter color
        message_text = record.getMessage()
        highlighted_message = (
            f"\033[1m\033[94m{message_text}\033[0m"  # Bold + Ocean Blue
        )

        # Replace the message in the JSON output
        json_output = json_output.replace(
            f'"{message_text}"', f'"{highlighted_message}"'
        )

        return f"{color}{json_output}{reset}"


def get_logger(name: str):
    log_level = logging.DEBUG if config["LOG_LEVEL"] == "hml" else logging.INFO

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    formatter = ColoredJSONFormatter(datefmt="%Y-%m-%dT%H:%M:%S")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if logger.hasHandlers():
        logger.handlers = [console_handler]

    return logger
