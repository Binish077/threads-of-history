from typing import Generator

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.infrastructure.db.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
	if SessionLocal is None:
		raise HTTPException(
			status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
			detail="Database is not configured",
		)

	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
