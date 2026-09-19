import heapq
from collections import defaultdict
from typing import Dict, List, Tuple

from app.domain.entities import EntityId
from app.domain.graph.temporal_graph import TemporalGraph


def degree_centrality(graph: TemporalGraph) -> Dict[EntityId, float]:
	"""Return normalized total degree for every entity in the directed graph."""
	node_count = len(graph.entities)
	if node_count <= 1:
		return {entity_id: 0.0 for entity_id in graph.entities}

	degrees = {entity_id: 0 for entity_id in graph.entities}
	for source_id, targets in graph.adj.items():
		for target_id in targets:
			if source_id in degrees and target_id in degrees:
				degrees[source_id] += 1
				degrees[target_id] += 1

	return {
		entity_id: degree / float(node_count - 1)
		for entity_id, degree in degrees.items()
	}


def betweenness_centrality(graph: TemporalGraph) -> Dict[EntityId, float]:
	"""Return normalized weighted betweenness centrality for each entity."""
	nodes = list(graph.entities)
	centrality = {entity_id: 0.0 for entity_id in nodes}
	weights = _edge_weights(graph)

	for source_id in nodes:
		predecessors = {entity_id: [] for entity_id in nodes}
		paths_count = dict.fromkeys(nodes, 0.0)
		paths_count[source_id] = 1.0
		distances = dict.fromkeys(nodes, float("inf"))
		distances[source_id] = 0.0
		order: List[EntityId] = []
		queue: List[Tuple[float, int, EntityId]] = [(0.0, 0, source_id)]
		sequence = 1

		while queue:
			distance, _, current_id = heapq.heappop(queue)
			if distance != distances[current_id]:
				continue
			order.append(current_id)
			for neighbor_id in graph.neighbors(current_id):
				if neighbor_id not in distances:
					continue
				candidate = distance + weights.get((current_id, neighbor_id), 1.0)
				if candidate < distances[neighbor_id]:
					distances[neighbor_id] = candidate
					heapq.heappush(queue, (candidate, sequence, neighbor_id))
					sequence += 1
					paths_count[neighbor_id] = paths_count[current_id]
					predecessors[neighbor_id] = [current_id]
				elif candidate == distances[neighbor_id]:
					paths_count[neighbor_id] += paths_count[current_id]
					predecessors[neighbor_id].append(current_id)

		dependency = dict.fromkeys(nodes, 0.0)
		while order:
			current_id = order.pop()
			for predecessor_id in predecessors[current_id]:
				dependency[predecessor_id] += (
					paths_count[predecessor_id]
					/ paths_count[current_id]
					* (1.0 + dependency[current_id])
				)
			if current_id != source_id:
				centrality[current_id] += dependency[current_id]

		normalization = (len(nodes) - 1) * (len(nodes) - 2)
	if normalization > 0:
		centrality = {
			entity_id: score / normalization
			for entity_id, score in centrality.items()
		}
	return centrality


def pagerank(
	graph: TemporalGraph,
	damping: float = 0.85,
	tolerance: float = 1e-12,
	max_iterations: int = 100,
) -> Dict[EntityId, float]:
	"""Return weighted PageRank scores using the graph's directed edges."""
	if not 0.0 < damping < 1.0:
		raise ValueError("damping must be between 0 and 1")

	nodes = list(graph.entities)
	if not nodes:
		return {}
	weights = _edge_weights(graph)
	probability = 1.0 / len(nodes)
	ranks = {entity_id: probability for entity_id in nodes}

	for _ in range(max_iterations):
		dangling_rank = sum(
		ranks[entity_id]
		for entity_id in nodes
		if not _outgoing_weights(graph, entity_id, weights)
		)
		updated = {
			entity_id: (1.0 - damping) * probability + damping * dangling_rank * probability
			for entity_id in nodes
		}
		for source_id in nodes:
			outgoing = _outgoing_weights(graph, source_id, weights)
			if not outgoing:
				continue
			weight_total = sum(outgoing.values())
			for target_id, weight in outgoing.items():
				updated[target_id] += damping * ranks[source_id] * weight / weight_total

			delta = sum(abs(updated[entity_id] - ranks[entity_id]) for entity_id in nodes)
		ranks = updated
		if delta < tolerance:
			break

	return ranks


def _edge_weights(graph: TemporalGraph) -> Dict[Tuple[EntityId, EntityId], float]:
	weights: Dict[Tuple[EntityId, EntityId], float] = {}
	for relationship in graph.relationships.values():
		if relationship.weight is None or relationship.weight <= 0:
			continue
		key = (relationship.source_id, relationship.target_id)
		weights[key] = max(weights.get(key, 0.0), relationship.weight)
	return weights


def _outgoing_weights(
	graph: TemporalGraph,
	source_id: EntityId,
	weights: Dict[Tuple[EntityId, EntityId], float],
) -> Dict[EntityId, float]:
	return {
		target_id: weights.get((source_id, target_id), 1.0)
		for target_id in graph.neighbors(source_id)
		if target_id in graph.entities
	}
