from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import List, Optional

from app.domain.entities import EntityId


class RelationshipType(str, Enum):
	MARRIAGE = "marriage"
	MOTHER_OF = "mother_of"
	FATHER_OF = "father_of"
	ALLIANCE = "alliance"
	POLITICAL_SUPPORT = "political_support"
	CLAIM = "claim"
	RIVALRY = "rivalry"
	FAMILY = "family"
	SPOUSE_OF = "spouse_of"
	SUCCEEDED = "succeeded"
	MEMBER_OF = "member_of"
	PARTICIPATED_IN = "participated_in"
	ALLIED_WITH = "allied_with"
	RIVAL_OF = "rival_of"
	CLAIMED_BY = "claimed_by"
	CONQUERED = "conquered"


@dataclass(frozen=True)
class Relationship:
	id: EntityId
	source_id: EntityId
	target_id: EntityId
	type: RelationshipType
	valid_from: Optional[date] = None
	valid_to: Optional[date] = None
	weight: float = 1.0
	confidence: float = 1.0
	source_ids: List[EntityId] = field(default_factory=list)
