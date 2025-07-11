from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
	DATABASE_URL:str

	model_config = SettingsConfigDict(env_file='.env')

settings = AppSettings()