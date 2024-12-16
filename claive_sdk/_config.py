# config.py

"""
Module Claive AI SDK configurations and constants
"""

import logging

LOG_LEVEL = 'CLAIVE_SDK_LOG_LEVEL' # log level env var

# Define a dictionary to map log level names to their corresponding logging levels
LOG_LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warn': logging.WARNING,
    'warning': logging.WARNING,  # Allow both 'warn' and 'warning' as valid values
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
    'fatal': logging.CRITICAL
}

API_KEY = 'CLAIVE_AI_API_KEY' # api key env var
