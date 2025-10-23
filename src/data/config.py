from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic import SecretStr

from pathlib import Path


BASE_PATH = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    POSTGRES_USER: SecretStr
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: SecretStr
    POSTGRES_HOST: SecretStr
    POSTGRES_PORT: SecretStr

    PRIVATE_KEY: SecretStr

    model_config = SettingsConfigDict(
        env_file = BASE_PATH / '.env'
    )

    @property
    def DB_URI(self):
        return(
            f"postgresql+asyncpg://{self.POSTGRES_USER.get_secret_value()}:"
            f"{self.POSTGRES_PASSWORD.get_secret_value()}"
            f"@{self.POSTGRES_HOST.get_secret_value()}:{self.POSTGRES_PORT.get_secret_value()}/{self.POSTGRES_DB.get_secret_value()}"
        )
    
settings = Settings()