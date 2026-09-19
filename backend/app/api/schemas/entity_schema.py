from datetime import date
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class EntityResponse(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: str
	type: str
	name: str
	valid_from: Optional[date] = None
	valid_to: Optional[date] = None
	attributes: Dict[str, Any] = Field(default_factory=dict)

	@field_validator("attributes", mode="before")
	@classmethod
	def default_missing_attributes(cls, value: Optional[Dict[str, Any]]) -> Dict[str, Any]:
		return value or {}


class RelationshipResponse(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: str
	source_id: str
	target_id: str
	type: str
	valid_from: Optional[date] = None
	valid_to: Optional[date] = None
	weight: float = 1.0
	confidence: float = 1.0


class EntityRelationshipsResponse(BaseModel):
	entity_id: str
	relationships: List[RelationshipResponse]
