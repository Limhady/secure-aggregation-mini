"""Utilities for pairwise mask generation.

This module implements a small teaching-oriented pairwise mask mechanism.
For every pair of clients (i, j), a deterministic random mask is generated.
Client i adds the mask and client j subtracts the same mask, so all masks
cancel out after server-side summation.
"""

from __future__ import annotations

import hashlib
from typing import Dict, Tuple

import numpy as np

Pair = Tuple[int, int]


def _pair_seed(client_a: int, client_b: int, base_seed: int) -> int:
    """Derive a stable integer seed for a client pair.

    Python's built-in hash is randomized between processes, so a SHA-256 based
    seed is used for reproducible classroom experiments.
    """

    left, right = sorted((client_a, client_b))
    token = f"{base_seed}:{left}:{right}".encode("utf-8")
    digest = hashlib.sha256(token).digest()
    return int.from_bytes(digest[:8], "big") % (2**32)


def generate_pairwise_masks(
    client_ids: list[int],
    vector_dim: int,
    base_seed: int,
    scale: float = 10.0,
) -> Dict[Pair, np.ndarray]:
    """Generate one random mask for every unordered pair of clients."""

    masks: Dict[Pair, np.ndarray] = {}
    ordered_ids = sorted(client_ids)

    for pos, client_i in enumerate(ordered_ids):
        for client_j in ordered_ids[pos + 1 :]:
            rng = np.random.default_rng(_pair_seed(client_i, client_j, base_seed))
            mask = rng.normal(loc=0.0, scale=scale, size=vector_dim)
            masks[(client_i, client_j)] = mask

    return masks


def mask_contribution_for_client(
    client_id: int,
    pairwise_masks: Dict[Pair, np.ndarray],
) -> np.ndarray:
    """Return the total mask contribution for a specific client."""

    contribution = None
    for (client_i, client_j), mask in pairwise_masks.items():
        if client_id == client_i:
            term = mask
        elif client_id == client_j:
            term = -mask
        else:
            continue

        contribution = term.copy() if contribution is None else contribution + term

    if contribution is None:
        raise ValueError(f"No pairwise masks found for client {client_id}")
    return contribution


def total_mask_residual(
    client_ids: list[int],
    pairwise_masks: Dict[Pair, np.ndarray],
) -> np.ndarray:
    """Compute the residual after summing all clients' mask contributions."""

    residual = None
    for client_id in client_ids:
        contribution = mask_contribution_for_client(client_id, pairwise_masks)
        residual = contribution.copy() if residual is None else residual + contribution
    return residual
