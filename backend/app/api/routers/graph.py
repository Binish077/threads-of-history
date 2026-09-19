from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.schemas.entity_schema import EntityResponse, RelationshipResponse
from app.api.schemas.graph_schema import GraphPathResponse, GraphSnapshotResponse
from app.domain.graph.temporal_graph import TemporalGraph
from app.domain.services.snapshot_service import SnapshotService
from app.infrastructure.repositories.entity_repo import EntityRepository
from app.infrastructure.repositories.relationship_repo import RelationshipRepository


router = APIRouter(prefix="/v1/graph", tags=["graph"])


@router.get("/snapshot", response_model=GraphSnapshotResponse)
def get_graph_snapshot(
	as_of: date = Query(..., alias="date"),
	db: Session = Depends(get_db),
) -> GraphSnapshotResponse:
	snapshot = SnapshotService(
		EntityRepository(db),
		RelationshipRepository(db),
	).create_snapshot(as_of)
	return GraphSnapshotResponse(
		as_of=snapshot.as_of,
		entities=[EntityResponse.model_validate(item) for item in snapshot.entities],
		relationships=[RelationshipResponse.model_validate(item) for item in snapshot.relationships],
	)


@router.get("/path", response_model=GraphPathResponse)
def get_graph_path(
	source: UUID,
	target: UUID,
	as_of: date = Query(..., alias="date"),
	db: Session = Depends(get_db),
) -> GraphPathResponse:
	snapshot = SnapshotService(
		EntityRepository(db),
		RelationshipRepository(db),
	).create_snapshot(as_of)
	graph = TemporalGraph.from_snapshot(snapshot)
	source_id = str(source)
	target_id = str(target)
	return GraphPathResponse(
		source_id=source_id,
		target_id=target_id,
		path=[str(entity_id) for entity_id in graph.path_between(source_id, target_id)],
	)
