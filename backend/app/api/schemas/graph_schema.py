from datetime import date
from typing import List

from pydantic import BaseModel

from app.api.schemas.entity_schema import EntityResponse, RelationshipResponse


class GraphSnapshotResponse(BaseModel):
	as_of: date
	entities: List[EntityResponse]
	relationships: List[RelationshipResponse]


class GraphPathResponse(BaseModel):
	source_id: str
	target_id: str
	path: List[str]
