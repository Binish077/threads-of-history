from datetime import date
from typing import List, Optional, Union
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infrastructure.db.models import EntityRecord


class EntityRepository:
	def __init__(self, session: Session):
		self.session = session

	def get_by_id(self, entity_id: Union[str, UUID]) -> Optional[EntityRecord]:
		statement = select(EntityRecord).where(EntityRecord.id == str(entity_id))
		return self.session.scalars(statement).one_or_none()

	def list(
		self,
		entity_type: Optional[str] = None,
		name: Optional[str] = None,
		) -> List[EntityRecord]:
		statement = select(EntityRecord).order_by(EntityRecord.name)
		if entity_type is not None:
			statement = statement.where(EntityRecord.type == entity_type)
		if name is not None:
			statement = statement.where(EntityRecord.name == name)
		return list(self.session.scalars(statement).all())

	def list_active_on(self, as_of: date) -> List[EntityRecord]:
		statement = (
			select(EntityRecord)
			.where(
				(EntityRecord.valid_from.is_(None) | (EntityRecord.valid_from <= as_of)),
				(EntityRecord.valid_to.is_(None) | (EntityRecord.valid_to >= as_of)),
			)
			.order_by(EntityRecord.name)
		)
		return list(self.session.scalars(statement).all())
