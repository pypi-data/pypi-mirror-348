"""
Core Strategy interface for Rock-Paper-Scissors.

Authors should subclass `Strategy`, set a unique `name` string,
and implement `play()` and `handle_moves()`. Optionally receive a pre-loaded
ML model via the `model` parameter.
"""

from abc import ABC, abstractmethod
from typing import ClassVar, Literal, Any

OPTIONS = Literal["rock", "paper", "scissors"]


class Strategy(ABC):
    """
    Base class for RPS strategies.

    Attributes:
        name: ClassVar[str] – must be overridden by each subclass.
        model: Any or None – optional ML artifact loaded externally.
    """

    name: ClassVar[str]
    model: Any

    def __init__(self, model: Any = None):
        """
        model: an optional object (e.g. a loaded TF/PyTorch/ONNX model).
        If your strategy doesn’t use a model, simply ignore this.
        """
        self.model = model

    @abstractmethod
    def play(self) -> OPTIONS:
        """
        Return one of "rock", "paper", or "scissors" for the next move.
        You may use `self.model` inside to compute a prediction.
        """
        ...

    @abstractmethod
    def handle_moves(self, own_move: OPTIONS, opponent_move: OPTIONS) -> None:
        """
        Called after each round. Update internal state (history, counters, etc.).
        """
        ...
