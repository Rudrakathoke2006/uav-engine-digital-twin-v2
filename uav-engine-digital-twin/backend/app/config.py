from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "AeroTwin-PX v2 FastAPI Backend"
    APP_ENV: str = "development"
    DATABASE_URL: str = "sqlite:///./aerotwin_mvp.db"
    JWT_SECRET: str = "defence-grade-secret-key-change-me"
    TELEMETRY_INTERVAL_MS: int = 1000
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000", "http://localhost:8501"]

    class Config:
        env_file = ".env"

settings = Settings()
