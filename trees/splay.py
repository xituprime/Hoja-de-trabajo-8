from typing import Tuple

from .abstract_tree import AbstractTree
from .node import Node
from .process import Process


class SplayTree(AbstractTree):
    """
    Splay Tree: árbol auto-ajustable. Cada vez que se accede a un nodo,
    se hace 'splay' (se mueve a la raíz) usando rotaciones Zig, Zig-Zig y Zig-Zag.
    Complejidad amortizada: O(log n) por operación.
    Ventaja: accesos frecuentes al mismo nodo son O(1) después del primer acceso.
    """

    def insert(self, process: Process) -> None:
        new_node = Node(process)

        if self.root is None:
            self.root = new_node
            return

        # Inserción BST estándar
        current = self.root
        while True:
            if process.vruntime < current.process.vruntime:
                if current.left is None:
                    current.left = new_node
                    new_node.parent = current
                    break
                current = current.left
            else:
                if current.right is None:
                    current.right = new_node
                    new_node.parent = current
                    break
                current = current.right

        # Después de insertar, hacemos splay del nuevo nodo
        self.splay(new_node)

    def search(self, vruntime: float) -> Tuple[Node | None, int]:
        """
        Busca el nodo. Si se encuentra, lo mueve a la raíz con splay.
        Retorna (nodo_encontrado, pasos).
        """
        steps = 0
        current = self.root
        last_visited = None

        while current is not None:
            last_visited = current
            if vruntime == current.process.vruntime:
                self.splay(current)
                return current, steps
            steps += 1
            if vruntime < current.process.vruntime:
                current = current.left
            else:
                current = current.right

        # Aunque no se encontró, hacemos splay del último nodo visitado
        if last_visited is not None:
            self.splay(last_visited)

        return None, steps

    def splay(self, node: Node) -> None:
        """
        Mueve `node` a la raíz del árbol mediante rotaciones.
        Casos: Zig (padre es raíz), Zig-Zig (mismo lado), Zig-Zag (lados opuestos).
        """
        while node.parent is not None:
            parent = node.parent
            grandparent = parent.parent

            if grandparent is None:
                # Caso Zig: el padre es la raíz
                if node == parent.left:
                    self.rotateRight(parent)
                else:
                    self.rotateLeft(parent)

            elif node == parent.left and parent == grandparent.left:
                # Caso Zig-Zig: node y parent ambos son hijos izquierdos
                self.rotateRight(grandparent)
                self.rotateRight(parent)

            elif node == parent.right and parent == grandparent.right:
                # Caso Zig-Zig: node y parent ambos son hijos derechos
                self.rotateLeft(grandparent)
                self.rotateLeft(parent)

            elif node == parent.right and parent == grandparent.left:
                # Caso Zig-Zag: node es hijo derecho, parent es hijo izquierdo
                self.rotateLeft(parent)
                self.rotateRight(grandparent)

            else:
                # Caso Zig-Zag: node es hijo izquierdo, parent es hijo derecho
                self.rotateRight(parent)
                self.rotateLeft(grandparent)

    def rotateLeft(self, node: Node) -> None:
        """
        Rotación izquierda alrededor de `node`.
        El hijo derecho de node sube y node baja a la izquierda.
        """
        right_child = node.right
        if right_child is None:
            return

        # El hijo izquierdo del hijo derecho pasa a ser el hijo derecho de node
        node.right = right_child.left
        if right_child.left is not None:
            right_child.left.parent = node

        # El hijo derecho toma el lugar de node
        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child

        right_child.left = node
        node.parent = right_child

    def rotateRight(self, node: Node) -> None:
        """
        Rotación derecha alrededor de `node`.
        El hijo izquierdo de node sube y node baja a la derecha.
        """
        left_child = node.left
        if left_child is None:
            return

        node.left = left_child.right
        if left_child.right is not None:
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
