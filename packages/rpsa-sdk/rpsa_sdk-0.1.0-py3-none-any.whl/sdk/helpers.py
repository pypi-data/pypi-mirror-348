"""
Utility helpers for common strategy patterns.
"""

import random
from typing import Literal, List, Tuple

OPTIONS = Literal["rock", "paper", "scissors"]


def random_move() -> OPTIONS:
    """Choose uniformly at random."""
    return random.choice(["rock", "paper", "scissors"])


def counter_move(move: OPTIONS) -> OPTIONS:
    """Return the move that beats the given move."""
    if move == "rock":
        return "paper"
    if move == "paper":
        return "scissors"
    return "rock"


def most_common(history: List[Tuple[OPTIONS, OPTIONS]], idx: int = 1) -> OPTIONS:
    """
    Given a list of (own, opponent) tuples, return
    the most frequent move seen at position `idx` (0 or 1).
    """
    counts = {"rock": 0, "paper": 0, "scissors": 0}
    for record in history:
        counts[record[idx]] += 1
    # tie-breaker: dict order, but rarely matters
    return max(counts, key=counts.get)
