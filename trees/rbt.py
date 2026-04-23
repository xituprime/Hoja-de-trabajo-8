from typing import Tuple

from .abstract_tree import AbstractTree
from .node import Node
from .process import Process


class RedBlackTree(AbstractTree):
    """
    Red-Black Tree: árbol auto-balanceado con 4 propiedades:
      1. Todo nodo es rojo o negro.
      2. La raíz siempre es negra.
      3. Todo nodo NULL (hoja sentinel) es negro.
      4. Si un nodo es rojo, sus dos hijos son negros.
      5. Para todo nodo, todos los caminos a sus hojas tienen la misma cantidad de nodos negros.

    Complejidad garantizada: O(log n) para inserción y búsqueda.
    Usado en el CFS de Linux para gestionar procesos por vruntime.
    """

    def __init__(self) -> None:
        super().__init__()
        # Nodo sentinel NULL: representa todas las hojas vacías (siempre negro)
        self.NIL: Node = Node(Process(-1, -1.0))
        self.NIL.is_red = False
        self.NIL.left = None
        self.NIL.right = None
        self.root = self.NIL

    def insert(self, process: Process) -> None:
        new_node = Node(process)
        new_node.left = self.NIL
        new_node.right = self.NIL
        new_node.is_red = True  # Todo nodo nuevo es rojo

        # Inserción BST estándar
        parent = None
        current = self.root

        while current != self.NIL:
            parent = current
            if process.vruntime < current.process.vruntime:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent

        if parent is None:
            self.root = new_node
        elif process.vruntime < parent.process.vruntime:
            parent.left = new_node
        else:
            parent.right = new_node

        # Si es la raíz, simplemente pintar de negro
        if new_node.parent is None:
            new_node.is_red = False
            return

        # Si el abuelo no existe (padre es raíz), no hay violaciones
        if new_node.parent.parent is None:
            return

        # Reparar violaciones de las propiedades Red-Black
        self._fix_insert(new_node)

    def _fix_insert(self, node: Node) -> None:
        """
        Corrige las violaciones de Red-Black después de una inserción.
        Un nodo rojo no puede tener un padre rojo (propiedad 4).
        """
        while node.parent is not None and node.parent.is_red:
            parent = node.parent
            grandparent = parent.parent

            if grandparent is None:
                break

            if parent == grandparent.left:
                uncle = grandparent.right

                if uncle != self.NIL and uncle.is_red:
                    # Caso 1: el tío es rojo → recolorear
                    parent.is_red = False
                    uncle.is_red = False
                    grandparent.is_red = True
                    node = grandparent
                else:
                    if node == parent.right:
                        # Caso 2: nodo es hijo derecho → rotar izquierda sobre padre
                        node = parent
                        self._rotateLeft(node)
                        parent = node.parent
                        grandparent = parent.parent if parent else None

                    # Caso 3: nodo es hijo izquierdo → rotar derecha sobre abuelo
                    if parent:
                        parent.is_red = False
                    if grandparent:
                        grandparent.is_red = True
                        self._rotateRight(grandparent)
            else:
                uncle = grandparent.left

                if uncle != self.NIL and uncle.is_red:
                    # Caso 1 (espejo): el tío es rojo → recolorear
                    parent.is_red = False
                    uncle.is_red = False
                    grandparent.is_red = True
                    node = grandparent
                else:
                    if node == parent.left:
                        # Caso 2 (espejo): nodo es hijo izquierdo → rotar derecha sobre padre
                        node = parent
                        self._rotateRight(node)
                        parent = node.parent
                        grandparent = parent.parent if parent else None

                    # Caso 3 (espejo): nodo es hijo derecho → rotar izquierda sobre abuelo
                    if parent:
                        parent.is_red = False
                    if grandparent:
                        grandparent.is_red = True
                        self._rotateLeft(grandparent)

            if node == self.root:
                break

        self.root.is_red = False  # La raíz siempre es negra

    def _rotateLeft(self, node: Node) -> None:
        right_child = node.right
        node.right = right_child.left

        if right_child.left != self.NIL:
            right_child.left.parent = node

        right_child.parent = node.parent

        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child

        right_child.left = node
        node.parent = right_child

    def _rotateRight(self, node: Node) -> None:
        left_child = node.left
        node.left = left_child.right

        if left_child.right != self.NIL:
            left_child.right.parent = node

        left_child.parent = node.parent

        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child

        left_child.right = node
        node.parent = left_child

    def search(self, vruntime: float) -> Tuple[Node | None, int]:
        """
        Búsqueda estándar BST (sin rotaciones, el RBT no altera la estructura en búsqueda).
        Retorna (nodo_encontrado, pasos).
        """
        steps = 0
        current = self.root

        while current != self.NIL and current is not None:
            if vruntime == current.process.vruntime:
                return current, steps
            steps += 1
            if vruntime < current.process.vruntime:
                current = current.left
            else:
                current = current.right

        return None, steps
