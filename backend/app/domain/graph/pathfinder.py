import heapq
from itertools import count
from typing import Dict, List, Tuple

from app.domain.entities import EntityId
from app.domain.graph.temporal_graph import TemporalGraph


class PathFinder:
	def __init__(self, graph: TemporalGraph) -> None:
		self.graph = graph

	def shortest_path(self, source_id: EntityId, target_id: EntityId) -> List[EntityId]:
		if source_id not in self.graph.entities or target_id not in self.graph.entities:
			return []
		if source_id == target_id:
			return [source_id]

		weights = self._edge_weights()
		distances: Dict[EntityId, float] = {source_id: 0.0}
		paths: Dict[EntityId, List[EntityId]] = {source_id: [source_id]}
		sequence = count()
		queue: List[Tuple[float, int, EntityId]] = [(0.0, next(sequence), source_id)]

		while queue:
			distance, _, current_id = heapq.heappop(queue)
			if distance != distances.get(current_id):
				continue
			if current_id == target_id:
				return paths[current_id]

			for neighbor_id in self.graph.neighbors(current_id):
				edge_weight = weights.get((current_id, neighbor_id), 1.0)
				candidate_distance = distance + edge_weight
				if candidate_distance < distances.get(neighbor_id, float("inf")):
					distances[neighbor_id] = candidate_distance
					paths[neighbor_id] = paths[current_id] + [neighbor_id]
					heapq.heappush(queue, (candidate_distance, next(sequence), neighbor_id))

		return []

	def find_path(self, source_id: EntityId, target_id: EntityId) -> List[EntityId]:
		return self.shortest_path(source_id, target_id)

	def _edge_weights(self) -> Dict[Tuple[EntityId, EntityId], float]:
		weights: Dict[Tuple[EntityId, EntityId], float] = {}
		for relationship in self.graph.relationships.values():
			if relationship.weight is None or relationship.weight <= 0:
				continue
			key = (relationship.source_id, relationship.target_id)
			weights[key] = min(weights.get(key, float("inf")), relationship.weight)
		return weights


def weighted_path(
	graph: TemporalGraph,
	source_id: EntityId,
	target_id: EntityId,
) -> List[EntityId]:
	return PathFinder(graph).shortest_path(source_id, target_id)
