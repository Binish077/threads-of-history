from datetime import date

from fastapi import APIRouter, HTTPException, Query, status

from app.api.schemas.graph_schema import GraphPathResponse, GraphSnapshotResponse


router = APIRouter(prefix="/v1/graph", tags=["graph"])


@router.get("/snapshot", response_model=GraphSnapshotResponse)
def get_graph_snapshot(as_of: date = Query(..., alias="date")) -> GraphSnapshotResponse:
	raise HTTPException(
		status_code=status.HTTP_501_NOT_IMPLEMENTED,
		detail="Graph snapshots are not implemented yet",
	)


@router.get("/path", response_model=GraphPathResponse)
def get_graph_path(source: str, target: str) -> GraphPathResponse:
	raise HTTPException(
		status_code=status.HTTP_501_NOT_IMPLEMENTED,
		detail="Graph pathfinding is not implemented yet",
	)
