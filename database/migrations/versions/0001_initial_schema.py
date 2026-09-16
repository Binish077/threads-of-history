"""Create the initial Threads of History schema.

Revision ID: 0001_initial_schema
Revises:
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "entities",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("type", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("valid_from", sa.Date()),
        sa.Column("valid_to", sa.Date()),
        sa.Column("attributes", postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.CheckConstraint("valid_to IS NULL OR valid_from IS NULL OR valid_to >= valid_from", name="ck_entities_valid_range"),
    )
    op.create_index("ix_entities_valid_dates", "entities", ["valid_from", "valid_to"])

    op.create_table(
        "relationships",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("source_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("entities.id", ondelete="CASCADE"), nullable=False),
        sa.Column("target_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("entities.id", ondelete="CASCADE"), nullable=False),
        sa.Column("type", sa.String(length=50), nullable=False),
        sa.Column("valid_from", sa.Date()),
        sa.Column("valid_to", sa.Date()),
        sa.Column("weight", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="1.0"),
        sa.CheckConstraint("valid_to IS NULL OR valid_from IS NULL OR valid_to >= valid_from", name="ck_relationships_valid_range"),
        sa.CheckConstraint("weight >= 0", name="ck_relationships_weight_nonnegative"),
        sa.CheckConstraint("confidence >= 0 AND confidence <= 1", name="ck_relationships_confidence_range"),
    )
    op.create_index("ix_relationships_valid_dates", "relationships", ["valid_from", "valid_to"])
    op.create_index("ix_relationships_source_id", "relationships", ["source_id"])
    op.create_index("ix_relationships_target_id", "relationships", ["target_id"])

    op.create_table(
        "sources",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("author", sa.String(length=255)),
        sa.Column("publication_date", sa.Date()),
        sa.Column("source_type", sa.String(length=50), nullable=False),
        sa.Column("citation", sa.Text()),
        sa.Column("metadata", postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
    )

    op.create_table(
        "entity_sources",
        sa.Column("entity_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("entities.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("source_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("sources.id", ondelete="CASCADE"), primary_key=True),
    )
    op.create_table(
        "relationship_sources",
        sa.Column("relationship_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("relationships.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("source_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("sources.id", ondelete="CASCADE"), primary_key=True),
    )

    op.create_table(
        "simulation_runs",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("scenario", sa.String(length=100), nullable=False),
        sa.Column("model", sa.String(length=100), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("iterations", sa.Integer(), nullable=False),
        sa.Column("seed", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.CheckConstraint("end_date >= start_date", name="ck_simulation_runs_date_range"),
        sa.CheckConstraint("iterations > 0", name="ck_simulation_runs_iterations_positive"),
    )
    op.create_table(
        "simulation_parameters",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("simulation_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("simulation_runs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("value", sa.Float(), nullable=False),
        sa.UniqueConstraint("simulation_id", "name", name="uq_simulation_parameter_name"),
    )
    op.create_table(
        "simulation_outcomes",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("simulation_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("simulation_runs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("label", sa.String(length=255), nullable=False),
        sa.Column("probability", sa.Float(), nullable=False),
        sa.Column("metadata", postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.CheckConstraint("probability >= 0 AND probability <= 1", name="ck_simulation_outcomes_probability_range"),
    )
    op.create_table(
        "simulation_events",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("simulation_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("simulation_runs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("actor_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("entities.id", ondelete="SET NULL")),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("details", postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
    )
    op.create_index("ix_simulation_events_simulation_id", "simulation_events", ["simulation_id"])


def downgrade() -> None:
    op.drop_index("ix_simulation_events_simulation_id", table_name="simulation_events")
    op.drop_table("simulation_events")
    op.drop_table("simulation_outcomes")
    op.drop_table("simulation_parameters")
    op.drop_table("simulation_runs")
    op.drop_table("relationship_sources")
    op.drop_table("entity_sources")
    op.drop_table("sources")
    op.drop_index("ix_relationships_target_id", table_name="relationships")
    op.drop_index("ix_relationships_source_id", table_name="relationships")
    op.drop_index("ix_relationships_valid_dates", table_name="relationships")
    op.drop_table("relationships")
    op.drop_index("ix_entities_valid_dates", table_name="entities")
    op.drop_table("entities")
