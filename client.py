"""Client implementation for the secure aggregation teaching demo."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np

from mask_utils import mask_contribution_for_client

Pair = Tuple[int, int]


@dataclass
class Client:
    """A simple federated learning client.

    The client owns a local update vector. Before sending it to the server, the
    client adds a pairwise mask contribution. The server sees only the masked
    vector.
    """

    client_id: int
    update: np.ndarray

    def masked_update(self, pairwise_masks: Dict[Pair, np.ndarray]) -> np.ndarray:
        """Return the masked update uploaded by this client."""

        return self.update + mask_contribution_for_client(self.client_id, pairwise_masks)

    def to_dict(self) -> dict:
        """Serialize client information for JSON output."""

        return {
            "client_id": self.client_id,
            "update": self.update.round(6).tolist(),
        }


def build_clients(
    num_clients: int,
    vector_dim: int,
    seed: int,
    update_scale: float,
) -> list[Client]:
    """Create clients with reproducible synthetic update vectors."""

    rng = np.random.default_rng(seed)
    clients: list[Client] = []

    for client_id in range(num_clients):
        update = rng.normal(loc=0.0, scale=update_scale, size=vector_dim)
        clients.append(Client(client_id=client_id, update=update))

    return clients
