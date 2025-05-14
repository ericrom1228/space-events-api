"""Settings for the app
Will read in settings in the following order:
- default variables
- environment file containing environment variables
- environment variables declared at runtime
"""
from datetime import datetime
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the app"""

    model_config = SettingsConfigDict(
        env_file="./.env",
        env_file_encoding="utf-8"
    )

    # Database
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_CONNECTION_TIMEOUT: int = 3000
    DB_NAME: str = "space_db"

    # Build information
    VERSION: str = "N/A"  # software version
    API_VERSION: str = "v1"  # api version
    BUILD_DATETIME: str = datetime.now().isoformat()  # date and time of build (ISO8601 Date Format)


settings = Settings()
