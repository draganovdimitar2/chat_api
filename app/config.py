from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):  # this class reads the .env variables
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRY: int
    model_config = SettingsConfigDict(
        env_file=".env",  # this tells the BaseSettings to read from .env file
        extra="ignore"  # ignoring extra attributes
    )


Config = Settings()  # import this for accessing .env variable
