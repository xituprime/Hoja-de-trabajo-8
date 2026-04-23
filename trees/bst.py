from .abstract_tree import AbstractTree
from .node import Node
from .process import Process


class BinarySearchTree(AbstractTree):
    """
    Árbol Binario de Búsqueda estándar (no balanceado).
    Complejidad teórica: O(log n) promedio, O(n) en el peor caso (entrada ordenada).
    """

    def insert(self, process: Process) -> None:
        new_node = Node(process)

        if self.root is None:
            self.root = new_node
            return

        current = self.root
        while True:
            if process.vruntime < current.process.vruntime:
                if current.left is None:
                    current.left = new_node
                    new_node.parent = current
                    return
                current = current.left
            else:
                if current.right is None:
                    current.right = new_node
                    new_node.parent = current
                    return
                current = current.right

    def search(self, vruntime: float) -> tuple[Node | None, int]:
        # Un paso = una comparación en un nodo (incluye la que encuentra el valor).
        steps = 0
        current = self.root

        while current is not None:
            steps += 1
            if vruntime == current.process.vruntime:
                return current, steps
            if vruntime < current.process.vruntime:
                current = current.left
            else:
                current = current.right

        return None, steps
