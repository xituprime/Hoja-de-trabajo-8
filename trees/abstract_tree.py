from abc import ABC, abstractmethod
from typing import Tuple

from .node import Node
from .process import Process


class AbstractTree(ABC):
    def __init__(self) -> None:
        self.root: Node | None = None

    @abstractmethod
    def insert(self, process: Process) -> None:
        pass

    @abstractmethod
    def search(self, vruntime: float) -> Tuple[Node | None, int]:
        """
        Returns (node_found, steps_count).
        steps_count increments each time we move left or right.
        """
        pass
