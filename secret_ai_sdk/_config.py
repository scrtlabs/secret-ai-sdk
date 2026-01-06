# config.py

"""
Module Secret AI SDK configurations and constants
"""

import logging

LOG_LEVEL = 'SECRET_SDK_LOG_LEVEL' # log level env var

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

API_KEY = 'SECRET_AI_API_KEY' # api key env var

# SECRET
SECRET_CHAIN_ID_DEFAULT = 'secret-4'
SECRET_WORKER_SMART_CONTRACT_DEFAULT = 'secret1xv90yettghx8uv6ug23knaf5mjqwlsghau6aqa'
SECRET_NODE_URL_DEFAULT = 'https://rpc12.scrtlabs.com/'

SECRET_CHAIN_ID = 'SECRET_CHAIN_ID' # points to the name of the env var for secret chain id
SECRET_WORKER_SMART_CONTRACT = 'SECRET_WORKER_SMART_CONTRACT' #points to the env var for the smart contract address for secret worker management
SECRET_NODE_URL = 'SECRET_NODE_URL' # points to the name of the env var for secret node url

# Network and Retry Configuration
REQUEST_TIMEOUT = 'SECRET_AI_REQUEST_TIMEOUT'  # env var for request timeout in seconds
REQUEST_TIMEOUT_DEFAULT = 30  # default timeout in seconds

CONNECT_TIMEOUT = 'SECRET_AI_CONNECT_TIMEOUT'  # env var for connection timeout in seconds
CONNECT_TIMEOUT_DEFAULT = 10  # default connection timeout in seconds

MAX_RETRIES = 'SECRET_AI_MAX_RETRIES'  # env var for max retry attempts
MAX_RETRIES_DEFAULT = 3  # default max retries

RETRY_DELAY = 'SECRET_AI_RETRY_DELAY'  # env var for initial retry delay in seconds
RETRY_DELAY_DEFAULT = 1  # default initial retry delay in seconds

RETRY_BACKOFF = 'SECRET_AI_RETRY_BACKOFF'  # env var for retry backoff multiplier
RETRY_BACKOFF_DEFAULT = 2  # default backoff multiplier

MAX_RETRY_DELAY = 'SECRET_AI_MAX_RETRY_DELAY'  # env var for max retry delay in seconds
MAX_RETRY_DELAY_DEFAULT = 30  # default max retry delay in seconds
