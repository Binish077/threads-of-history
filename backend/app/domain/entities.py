from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Any, Dict, Optional, Union
from uuid import UUID


class EntityType(str, Enum):
	PERSON = "person"
	HOUSE = "house"
	EVENT = "event"
	PLACE = "place"
	DYNASTY = "dynasty"
	POLITICAL_ENTITY = "political_entity"
	INSTITUTION = "institution"
	BATTLE = "battle"
	DOCUMENT = "document"


EntityId = Union[str, UUID]


@dataclass(frozen=True)
class Entity:
	id: EntityId
	type: EntityType
	name: str
	valid_from: Optional[date] = None
	valid_to: Optional[date] = None
	attributes: Dict[str, Any] = field(default_factory=dict)
