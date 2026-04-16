from abc import ABC, abstractmethod

from .node import Node
from .process import Process


class AbstractTree(ABC):
    def __init__(self) -> None:
        self.root: Node | None = None

    @abstractmethod
    def insert(self, process: Process) -> None:
        # Se implementará la inserción en el árbol
        pass

    @abstractmethod
    def search(self, vruntime: float) -> Node | None:
        # Se implementará la búsqueda en el árbol
        pass

