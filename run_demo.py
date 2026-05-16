"""Run a complete secure aggregation demo."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import config
from client import build_clients
from mask_utils import generate_pairwise_masks, total_mask_residual
from server import Server


def round_vector(vector: np.ndarray) -> list[float]:
    """Convert a vector to a rounded list for readable output."""

    return vector.round(6).tolist()


def main() -> None:
    output_dir = Path(config.OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    clients = build_clients(
        num_clients=config.NUM_CLIENTS,
        vector_dim=config.VECTOR_DIM,
        seed=config.RANDOM_SEED,
        update_scale=config.UPDATE_SCALE,
    )
    client_ids = [client.client_id for client in clients]

    pairwise_masks = generate_pairwise_masks(
        client_ids=client_ids,
        vector_dim=config.VECTOR_DIM,
        base_seed=config.RANDOM_SEED,
    )

    server = Server()
    for client in clients:
        server.receive(client.client_id, client.masked_update(pairwise_masks))

    secure_sum = server.aggregate()
    plain_sum = np.sum([client.update for client in clients], axis=0)
    mask_residual = total_mask_residual(client_ids, pairwise_masks)
    aggregation_error = np.linalg.norm(secure_sum - plain_sum)

    result = {
        "num_clients": config.NUM_CLIENTS,
        "vector_dim": config.VECTOR_DIM,
        "plain_client_updates": [client.to_dict() for client in clients],
        "masked_uploads_seen_by_server": server.masked_uploads_as_dict(),
        "plain_sum": round_vector(plain_sum),
        "secure_aggregation_sum": round_vector(secure_sum),
        "mask_residual": round_vector(mask_residual),
        "aggregation_l2_error": float(round(aggregation_error, 12)),
    }

    output_path = output_dir / config.RESULT_FILE
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print("Secure aggregation demo finished.")
    print(f"Number of clients: {config.NUM_CLIENTS}")
    print(f"Vector dimension: {config.VECTOR_DIM}")
    print(f"Plain sum: {round_vector(plain_sum)}")
    print(f"Secure aggregation sum: {round_vector(secure_sum)}")
    print(f"Mask residual: {round_vector(mask_residual)}")
    print(f"Aggregation L2 error: {aggregation_error:.12f}")
    print(f"Result saved to: {output_path}")


if __name__ == "__main__":
    main()
