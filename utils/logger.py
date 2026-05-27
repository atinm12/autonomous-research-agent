from loguru import logger
import os

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logger to write to file
logger.add(
    "logs/agent.log",
    rotation="10 MB",
    retention="7 days",
    level="INFO"
)

def log_info(message: str):
    """
    Logs general informational messages
    Example: "Calling LLM", "Retrieving SEC filing"
    """
    logger.info(message)


def log_error(message: str):
    """
    Logs errors
    Example: API failure, parsing failure, tool crash
    """
    logger.error(message)


def log_debug(message: str):
    """
    Logs debugging details
    Example: intermediate outputs, variables, tool traces
    """
    logger.debug(message)