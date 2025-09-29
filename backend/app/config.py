"""
Configuration settings for the application.
Uses Pydantic's BaseSettings to load environment variables.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Defines the environment variables required by the application.
    Pydantic will automatically read these from the environment.
    """
    DATABASE_URL: str

    # This tells Pydantic to look for a .env file if the variables aren't in the environment.
    # While Docker Compose provides them, this is good practice for local development.
    model_config = SettingsConfigDict(env_file=".env")


# This is the crucial line that was missing.
# We are creating an instance of the Settings class that the rest of our app can import and use.
settings = Settings()

