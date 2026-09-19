from fastapi import APIRouter, HTTPException, status

from app.api.schemas.entity_schema import EntityRelationshipsResponse, EntityResponse


router = APIRouter(prefix="/v1/entities", tags=["entities"])


@router.get("/{entity_id}", response_model=EntityResponse)
def get_entity(entity_id: str) -> EntityResponse:
	raise HTTPException(
		status_code=status.HTTP_501_NOT_IMPLEMENTED,
		detail="Entity retrieval is not implemented yet",
	)


@router.get("/{entity_id}/relationships", response_model=EntityRelationshipsResponse)
def get_entity_relationships(entity_id: str) -> EntityRelationshipsResponse:
	raise HTTPException(
		status_code=status.HTTP_501_NOT_IMPLEMENTED,
		detail="Entity relationship retrieval is not implemented yet",
	)
