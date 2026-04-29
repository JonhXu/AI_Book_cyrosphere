from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    app_name: str = "冰冻圈科学课堂虚拟助教"
    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com"
    deepseek_model: str = "deepseek-chat"
    app_database_path: Path = PROJECT_ROOT / "data" / "app.db"
    book_pdf_path: Path = PROJECT_ROOT / "冰冻圈科学-秦大河.pdf"
    book_collection_name: str = "cryosphere_science_qin_dahe"
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8000",
        "null",
    ]

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / "backend" / ".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
