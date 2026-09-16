import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _parse_origins(value: str) -> list[str]:
	return [origin.strip() for origin in value.split(",") if origin.strip()]


@dataclass(frozen=True)
class Settings:
	app_name: str = os.getenv("APP_NAME", "Threads of History")
	app_version: str = os.getenv("APP_VERSION", "0.1.0")
	environment: str = os.getenv("ENVIRONMENT", "development")
	database_url: str = os.getenv("DATABASE_URL", "")
	frontend_origins: list[str] = None  # type: ignore[assignment]

	def __post_init__(self) -> None:
		if self.frontend_origins is None:
			object.__setattr__(
				self,
				"frontend_origins",
				_parse_origins(
					os.getenv("FRONTEND_ORIGINS", "http://localhost:3000")
				),
			)


settings = Settings()
