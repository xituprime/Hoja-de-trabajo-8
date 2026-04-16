from .process import Process


class Node:
    def __init__(self, process: Process) -> None:
        # Se implementará la relación con otros nodos
        self.process: Process = process
        self.left: "Node | None" = None
        self.right: "Node | None" = None
        self.parent: "Node | None" = None

