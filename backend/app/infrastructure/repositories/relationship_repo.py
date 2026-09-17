from datetime import date
from typing import List, Optional, Union
from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.infrastructure.db.models import RelationshipRecord


class RelationshipRepository:
	def __init__(self, session: Session):
		self.session = session

	def get_by_id(self, relationship_id: Union[str, UUID]) -> Optional[RelationshipRecord]:
		statement = select(RelationshipRecord).where(RelationshipRecord.id == str(relationship_id))
		return self.session.scalars(statement).one_or_none()

	def list_active_on(self, as_of: date) -> List[RelationshipRecord]:
		statement = (
			select(RelationshipRecord)
			.where(
				(
					RelationshipRecord.valid_from.is_(None)
					| (RelationshipRecord.valid_from <= as_of)
				),
				(
					RelationshipRecord.valid_to.is_(None)
					| (RelationshipRecord.valid_to >= as_of)
				),
			)
			.order_by(RelationshipRecord.type, RelationshipRecord.id)
		)
		return list(self.session.scalars(statement).all())

	def list_for_entity(
		self,
		entity_id: Union[str, UUID],
		as_of: Optional[date] = None,
		) -> List[RelationshipRecord]:
		statement = select(RelationshipRecord).where(
			or_(
				RelationshipRecord.source_id == str(entity_id),
				RelationshipRecord.target_id == str(entity_id),
			)
		)
		if as_of is not None:
			statement = statement.where(
				(
					RelationshipRecord.valid_from.is_(None)
					| (RelationshipRecord.valid_from <= as_of)
				),
				(
					RelationshipRecord.valid_to.is_(None)
					| (RelationshipRecord.valid_to >= as_of)
				),
			)
		statement = statement.order_by(RelationshipRecord.type, RelationshipRecord.id)
		return list(self.session.scalars(statement).all())

	def list_between(
		self,
		source_id: Union[str, UUID],
		target_id: Union[str, UUID],
		as_of: Optional[date] = None,
	) -> list[RelationshipRecord]:
		statement = select(RelationshipRecord).where(
			RelationshipRecord.source_id == str(source_id),
			RelationshipRecord.target_id == str(target_id),
		)
		if as_of is not None:
			statement = statement.where(
				(
					RelationshipRecord.valid_from.is_(None)
					| (RelationshipRecord.valid_from <= as_of)
				),
				(
					RelationshipRecord.valid_to.is_(None)
					| (RelationshipRecord.valid_to >= as_of)
				),
			)
		return list(self.session.scalars(statement).all())
