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

    model_config = {"env_prefix": "METAAUDIT_"}

    @property
    def db_path(self) -> Path:
        return self.data_dir / "metaaudit.sqlite3"

    @property
    def documents_dir(self) -> Path:
        return self.data_dir / "documents"


settings = Settings()
