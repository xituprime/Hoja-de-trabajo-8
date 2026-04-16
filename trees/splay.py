from .abstract_tree import AbstractTree
from .node import Node
from .process import Process


class SplayTree(AbstractTree):
    def insert(self, process: Process) -> None:
        # Se implementará la inserción Splay
        pass

    def search(self, vruntime: float) -> Node | None:
        # Se implementará la búsqueda Splay
        pass

    def splay(self, node: Node) -> None:
        # Se implementará la operación splay
        pass

    def rotateLeft(self, node: Node) -> None:
        # Se implementará la rotación izquierda
        pass

    def rotateRight(self, node: Node) -> None:
        # Se implementará la rotación derecha
        pass

