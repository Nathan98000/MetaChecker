from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Runtime configuration.

    METAAUDIT_DATA_DIR holds everything the app persists: the SQLite database
    and the content-addressed document store. In the packaged desktop app the
    Tauri shell sets this to the platform app-data directory.
    """

    data_dir: Path = Path("var/data")
    run_worker: bool = True
    worker_poll_seconds: float = 0.5
    job_lease_seconds: float = 60.0
    job_max_attempts: int = 3

    # backend/.env is the sanctioned local-secret mechanism (gitignored).
    # The Anthropic key is read by the SDK/provider from ANTHROPIC_API_KEY;
    # it is never stored in the DB, logs, fixtures, or error messages.
    model_config = {
        "env_prefix": "METAAUDIT_",
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }

    @property
    def db_path(self) -> Path:
        return self.data_dir / "metaaudit.sqlite3"

    @property
    def documents_dir(self) -> Path:
        return self.data_dir / "documents"


settings = Settings()
