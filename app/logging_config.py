import logging.config
import yaml
from app.settings import settings  # Assuming settings are defined here


def get_logging_config() -> dict:
    """Load logging configuration from the YAML file."""
    with open("logging.yaml", "r") as f:
        config = yaml.safe_load(f)

    # Optionally, you can modify the config based on settings or environment variables
    if settings.LOG_TO_FILE:
        config['handlers']['console']['stream'] = 'ext://sys.stderr'
        config['handlers']['file']['filename'] = settings.LOG_FILE_PATH
        config['root']['level'] = settings.LOG_LEVEL
        config['loggers']['app']['level'] = settings.LOG_LEVEL

    return config


def configure_logging():
    """Configure logging using the loaded config."""
    logging.config.dictConfig(get_logging_config())
