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
SECRET_CHAIN_ID_DEFAULT = 'pulsar-3'
SECRET_WORKER_SMART_CONTRACT_DEFAULT = 'secret18cy3cgnmkft3ayma4nr37wgtj4faxfnrnngrlq'
SECRET_NODE_URL_DEFAULT = 'https://pulsar.lcd.secretnodes.com'

SECRET_CHAIN_ID = 'SECRET_CHAIN_ID' # points to the name of the env var for secret chain id
SECRET_WORKER_SMART_CONTRACT = 'SECRET_WORKER_SMART_CONTRACT' #points to the env var for the smart contract address for secret worker management
SECRET_NODE_URL = 'SECRET_NODE_URL' # points to the name of the env var for secret node url
