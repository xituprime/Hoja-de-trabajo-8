from abc import ABC, abstractmethod

from .node import Node
from .process import Process


class AbstractTree(ABC):
    def __init__(self) -> None:
        self.root: Node | None = None

    @abstractmethod
    def insert(self, process: Process) -> None:
        pass

    @abstractmethod
    def search(self, vruntime: float) -> tuple[Node | None, int]:
        pass
