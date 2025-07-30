from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./app.db"
    secret_key: str = "CHANGE_ME"  # 生產環境請使用 env 設定
    access_token_expire_minutes: int = 30
    algorithm: str = "HS256"
    debug: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings() 