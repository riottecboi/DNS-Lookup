from pydantic_settings import BaseSettings
class Settings(BaseSettings):


    class Config:
        env_file = 'settings.cfg'

settings = Settings()