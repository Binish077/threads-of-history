from datetime import date, datetime
from typing import Dict, Optional
from uuid import uuid4

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
	pass


class EntityRecord(Base):
	__tablename__ = "entities"

	id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
	type: Mapped[str] = mapped_column(String(50), nullable=False)
	name: Mapped[str] = mapped_column(String(255), nullable=False)
	valid_from: Mapped[Optional[date]] = mapped_column(Date)
	valid_to: Mapped[Optional[date]] = mapped_column(Date)
	attributes: Mapped[Dict] = mapped_column(JSONB, nullable=False, default=dict)
	created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class RelationshipRecord(Base):
	__tablename__ = "relationships"

	id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
	source_id: Mapped[str] = mapped_column(ForeignKey("entities.id", ondelete="CASCADE"), nullable=False)
	target_id: Mapped[str] = mapped_column(ForeignKey("entities.id", ondelete="CASCADE"), nullable=False)
	type: Mapped[str] = mapped_column(String(50), nullable=False)
	valid_from: Mapped[Optional[date]] = mapped_column(Date)
	valid_to: Mapped[Optional[date]] = mapped_column(Date)
	weight: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
	confidence: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)


class SourceRecord(Base):
	__tablename__ = "sources"

	id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
	title: Mapped[str] = mapped_column(String(500), nullable=False)
	author: Mapped[Optional[str]] = mapped_column(String(255))
	publication_date: Mapped[Optional[date]] = mapped_column(Date)
	source_type: Mapped[str] = mapped_column(String(50), nullable=False)
	citation: Mapped[Optional[str]] = mapped_column(Text)
	metadata_: Mapped[Dict] = mapped_column("metadata", JSONB, nullable=False, default=dict)


class EntitySourceRecord(Base):
	__tablename__ = "entity_sources"

	entity_id: Mapped[str] = mapped_column(ForeignKey("entities.id", ondelete="CASCADE"), primary_key=True)
	source_id: Mapped[str] = mapped_column(ForeignKey("sources.id", ondelete="CASCADE"), primary_key=True)


class RelationshipSourceRecord(Base):
	__tablename__ = "relationship_sources"

	relationship_id: Mapped[str] = mapped_column(ForeignKey("relationships.id", ondelete="CASCADE"), primary_key=True)
	source_id: Mapped[str] = mapped_column(ForeignKey("sources.id", ondelete="CASCADE"), primary_key=True)


class SimulationRunRecord(Base):
	__tablename__ = "simulation_runs"

	id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
	scenario: Mapped[str] = mapped_column(String(100), nullable=False)
	model: Mapped[str] = mapped_column(String(100), nullable=False)
	start_date: Mapped[date] = mapped_column(Date, nullable=False)
	end_date: Mapped[date] = mapped_column(Date, nullable=False)
	iterations: Mapped[int] = mapped_column(Integer, nullable=False)
	seed: Mapped[int] = mapped_column(Integer, nullable=False)
	status: Mapped[str] = mapped_column(String(30), nullable=False, default="pending")
	created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class SimulationParameterRecord(Base):
	__tablename__ = "simulation_parameters"

	id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
	simulation_id: Mapped[str] = mapped_column(ForeignKey("simulation_runs.id", ondelete="CASCADE"), nullable=False)
	name: Mapped[str] = mapped_column(String(100), nullable=False)
	value: Mapped[float] = mapped_column(Float, nullable=False)


class SimulationOutcomeRecord(Base):
	__tablename__ = "simulation_outcomes"

	id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
	simulation_id: Mapped[str] = mapped_column(ForeignKey("simulation_runs.id", ondelete="CASCADE"), nullable=False)
	label: Mapped[str] = mapped_column(String(255), nullable=False)
	probability: Mapped[float] = mapped_column(Float, nullable=False)
	metadata_: Mapped[Dict] = mapped_column("metadata", JSONB, nullable=False, default=dict)


class SimulationEventRecord(Base):
	__tablename__ = "simulation_events"

	id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
	simulation_id: Mapped[str] = mapped_column(ForeignKey("simulation_runs.id", ondelete="CASCADE"), nullable=False)
	timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
	actor_id: Mapped[Optional[str]] = mapped_column(ForeignKey("entities.id", ondelete="SET NULL"))
	event_type: Mapped[str] = mapped_column(String(100), nullable=False)
	details: Mapped[Dict] = mapped_column(JSONB, nullable=False, default=dict)
