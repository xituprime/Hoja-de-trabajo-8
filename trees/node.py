from .process import Process


class Node:
    def __init__(self, process: Process) -> None:
        self.process: Process = process
        self.left: "Node | None" = None
        self.right: "Node | None" = None
        self.parent: "Node | None" = None

    def __repr__(self) -> str:
        return f"Node(vruntime={self.process.vruntime:.2f})"
