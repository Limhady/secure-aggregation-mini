"""Compare plain aggregation with secure aggregation."""

from __future__ import annotations

import numpy as np

import config
from client import build_clients
from mask_utils import generate_pairwise_masks
from server import Server


def fmt(vector: np.ndarray) -> str:
    """Format a vector for console display."""

    return np.array2string(vector.round(4), separator=", ")


def main() -> None:
    clients = build_clients(
        num_clients=config.NUM_CLIENTS,
        vector_dim=config.VECTOR_DIM,
        seed=config.RANDOM_SEED,
        update_scale=config.UPDATE_SCALE,
    )
    client_ids = [client.client_id for client in clients]
    pairwise_masks = generate_pairwise_masks(client_ids, config.VECTOR_DIM, config.RANDOM_SEED)

    print("=== Plain aggregation view ===")
    for client in clients:
        print(f"client {client.client_id} true update:  {fmt(client.update)}")
    plain_sum = np.sum([client.update for client in clients], axis=0)
    print(f"plain sum:              {fmt(plain_sum)}")

    print("\n=== Secure aggregation view ===")
    server = Server()
    for client in clients:
        masked = client.masked_update(pairwise_masks)
        server.receive(client.client_id, masked)
        print(f"client {client.client_id} masked upload: {fmt(masked)}")

    secure_sum = server.aggregate()
    print(f"secure aggregated sum:  {fmt(secure_sum)}")
    print(f"difference norm:        {np.linalg.norm(secure_sum - plain_sum):.12f}")


if __name__ == "__main__":
    main()
