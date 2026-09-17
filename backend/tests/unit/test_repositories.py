from datetime import date
from unittest.mock import MagicMock

from sqlalchemy.dialects import postgresql

from app.infrastructure.db.models import EntityRecord, RelationshipRecord
from app.infrastructure.repositories.entity_repo import EntityRepository
from app.infrastructure.repositories.relationship_repo import RelationshipRepository


def compile_statement(statement) -> str:
	return str(statement.compile(dialect=postgresql.dialect()))


def test_entity_repository_get_by_id_returns_record() -> None:
	session = MagicMock()
	record = EntityRecord(name="Rhaenyra Targaryen")
	session.scalars.return_value.one_or_none.return_value = record
	repository = EntityRepository(session)

	result = repository.get_by_id("entity-id")

	assert result is record
	session.scalars.assert_called_once()
	assert "entities.id" in compile_statement(session.scalars.call_args.args[0])


def test_entity_repository_list_active_on_contains_inclusive_date_filters() -> None:
	session = MagicMock()
	session.scalars.return_value.all.return_value = []
	repository = EntityRepository(session)

	repository.list_active_on(date(125, 1, 1))

	statement = session.scalars.call_args.args[0]
	compiled = compile_statement(statement)
	assert "valid_from" in compiled
	assert "valid_to" in compiled
	assert " <= " in compiled
	assert " >= " in compiled


def test_relationship_repository_filters_entity_and_date() -> None:
	session = MagicMock()
	session.scalars.return_value.all.return_value = []
	repository = RelationshipRepository(session)

	repository.list_for_entity("entity-id", date(125, 1, 1))

	compiled = compile_statement(session.scalars.call_args.args[0])
	assert "source_id" in compiled
	assert "target_id" in compiled
	assert "valid_from" in compiled
	assert "valid_to" in compiled


def test_relationship_repository_list_between_returns_records() -> None:
	session = MagicMock()
	record = RelationshipRecord(type="father_of")
	session.scalars.return_value.all.return_value = [record]
	repository = RelationshipRepository(session)

	result = repository.list_between("source-id", "target-id")

	assert result == [record]
	compiled = compile_statement(session.scalars.call_args.args[0])
	assert "source_id" in compiled
	assert "target_id" in compiled