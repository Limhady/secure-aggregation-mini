"""Server implementation for the secure aggregation teaching demo."""

from __future__ import annotations

import numpy as np


class Server:
    """A minimal aggregation server.

    The server receives only masked client updates. It aggregates them by
    summation and does not need to know the pairwise masks.
    """

    def __init__(self) -> None:
        self.received_updates: dict[int, np.ndarray] = {}

    def receive(self, client_id: int, masked_update: np.ndarray) -> None:
        """Store a masked update from a client."""

        self.received_updates[client_id] = masked_update

    def aggregate(self) -> np.ndarray:
        """Aggregate all received masked updates."""

        if not self.received_updates:
            raise RuntimeError("No updates received by the server.")

        updates = list(self.received_updates.values())
        return np.sum(updates, axis=0)

    def masked_uploads_as_dict(self) -> dict:
        """Serialize masked uploads for JSON output."""

        return {
            str(client_id): update.round(6).tolist()
            for client_id, update in sorted(self.received_updates.items())
        }
