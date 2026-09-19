from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.schemas.entity_schema import (
	EntityRelationshipsResponse,
	EntityResponse,
	RelationshipResponse,
)
from app.infrastructure.repositories.entity_repo import EntityRepository
from app.infrastructure.repositories.relationship_repo import RelationshipRepository


router = APIRouter(prefix="/v1/entities", tags=["entities"])


@router.get("/{entity_id}", response_model=EntityResponse)
def get_entity(entity_id: UUID, db: Session = Depends(get_db)) -> EntityResponse:
	entity = EntityRepository(db).get_by_id(entity_id)
	if entity is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entity not found")
	return EntityResponse.model_validate(entity)


@router.get("/{entity_id}/relationships", response_model=EntityRelationshipsResponse)
def get_entity_relationships(
	entity_id: UUID,
	as_of: date = Query(None, alias="date"),
	db: Session = Depends(get_db),
) -> EntityRelationshipsResponse:
	entity = EntityRepository(db).get_by_id(entity_id)
	if entity is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entity not found")

	relationships = RelationshipRepository(db).list_for_entity(entity_id, as_of)
	return EntityRelationshipsResponse(
		entity_id=str(entity_id),
		relationships=[RelationshipResponse.model_validate(item) for item in relationships],
	)
