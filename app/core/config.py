from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
	DATABASE_USER: str
	DATABASE_PASSWORD: str
	DATABASE_URL: str
	SECRET_KEY: str
	ALGORITHM: str
	ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

	model_config = SettingsConfigDict(env_file='.env')

settings = AppSettings()
