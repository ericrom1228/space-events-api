from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import datetime


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file="./.env",
        env_file_encoding="utf-8"
    )

    # Database
    MONGO_URI: str = "mongodb://localhost:27017"
    DB_NAME: str = "space_db"

    # Build information
    VERSION: str = "N/A"  # software version
    API_VERSION: str = "v1"  # api version
    BUILD_DATETIME: str = datetime.now().isoformat()  # date and time of build in ISO8601 Date Format


settings = Settings()