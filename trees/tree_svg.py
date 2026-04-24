"""
Exporta la estructura de un arbol (BST, Splay o RBT) a SVG mediante recorrido.
No modifica el arbol; solo lee root, hijos y atributos opcionales (p. ej. is_red, NIL).
"""
from __future__ import annotations

from collections import deque
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape

from .node import Node


def _nil(tree: Any) -> Node | None:
    return getattr(tree, "NIL", None)


def _absent(node: Node | None, nil: Node | None) -> bool:
    if node is None:
        return True
    if nil is not None and node is nil:
        return True
    return False


def _left_child(n: Node, nil: Node | None) -> Node | None:
    L = n.left
    return None if _absent(L, nil) else L


def _right_child(n: Node, nil: Node | None) -> Node | None:
    R = n.right
    return None if _absent(R, nil) else R


def _inorder_nodes(root: Node | None, nil: Node | None) -> list[Node]:
    """Inorden iterativo (evita RecursionError en arboles muy profundos)."""
    out: list[Node] = []
    if _absent(root, nil):
        return out
    stack: list[Node] = []
    cur: Node | None = root
    while stack or cur is not None:
        while cur is not None:
            stack.append(cur)
            cur = _left_child(cur, nil)
        cur = stack.pop()
        out.append(cur)
        cur = _right_child(cur, nil)
    return out


def _depths(root: Node | None, nil: Node | None) -> dict[int, int]:
    """Profundidad BFS (sin recursion)."""
    depths: dict[int, int] = {}
    if _absent(root, nil):
        return depths
    q: deque[tuple[Node, int]] = deque([(root, 0)])
    while q:
        n, d = q.popleft()
        depths[id(n)] = d
        L = _left_child(n, nil)
        R = _right_child(n, nil)
        if L is not None:
            q.append((L, d + 1))
        if R is not None:
            q.append((R, d + 1))
    return depths


def write_tree_svg(
    tree: Any,
    path: str | Path,
    *,
    title: str = "",
    node_spacing: float = 10.0,
    level_height: float = 36.0,
    margin: float = 40.0,
    r_node: float = 5.0,
    max_depth: int | None = None,
) -> None:
    """
    Genera un SVG con nodos (circulos) y aristas (lineas).
    max_depth: si no es None, solo se dibujan nodos con profundidad <= max_depth
               (porcion representativa de arboles muy grandes).
    """
    path = Path(path)
    nil = _nil(tree)
    root = tree.root

    if _absent(root, nil):
        svg = _empty_svg(title or "Arbol vacio")
        path.write_text(svg, encoding="utf-8")
        return

    nodes = _inorder_nodes(root, nil)
    depths = _depths(root, nil)

    if max_depth is not None:
        nodes = [n for n in nodes if depths.get(id(n), 0) <= max_depth]

    if not nodes:
        path.write_text(_empty_svg(title or "Sin nodos en rango"), encoding="utf-8")
        return

    x_index = {id(n): i for i, n in enumerate(nodes)}
    positions: dict[int, tuple[float, float]] = {}
    for n in nodes:
        xi = x_index[id(n)]
        d = depths[id(n)]
        cx = margin + xi * node_spacing
        cy = margin + d * level_height
        positions[id(n)] = (cx, cy)

    max_x = margin + (len(nodes) - 1) * node_spacing + margin
    max_y = margin + max(depths[id(n)] for n in nodes) * level_height + margin + 24

    lines: list[str] = []
    circles: list[str] = []
    texts: list[str] = []

    for n in nodes:
        cx, cy = positions[id(n)]
        parent = n.parent
        if parent is not None and not _absent(parent, nil) and id(parent) in positions:
            px, py = positions[id(parent)]
            lines.append(
                f'<line x1="{px:.2f}" y1="{py:.2f}" x2="{cx:.2f}" y2="{cy:.2f}" '
                f'stroke="#333" stroke-width="1.2"/>'
            )

        is_red = bool(getattr(n, "is_red", False))
        fill = "#e74c3c" if is_red else "#34495e"
        stroke = "#c0392b" if is_red else "#1a252f"
        circles.append(
            f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r_node}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
        )
        label = f"p{n.process.pid}"
        texts.append(
            f'<text x="{cx:.2f}" y="{cy + 4:.2f}" text-anchor="middle" '
            f'font-size="7" font-family="Consolas,monospace" fill="#fff">{escape(label)}</text>'
        )

    title_el = ""
    if title:
        title_el = (
            f'<text x="{max_x / 2:.2f}" y="{18:.2f}" text-anchor="middle" '
            f'font-size="12" font-family="Arial,sans-serif" fill="#222">{escape(title)}</text>'
        )

    w = max(max_x, 200)
    h = max(max_y, 80)

    svg_parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" '
        f'viewBox="0 0 {w:.2f} {h:.2f}">',
        '<rect width="100%" height="100%" fill="#fafafa"/>',
        title_el,
        "<g>",
        *lines,
        *circles,
        *texts,
        "</g>",
        "</svg>",
    ]
    path.write_text("\n".join(svg_parts), encoding="utf-8")


def _empty_svg(msg: str) -> str:
    return "\n".join(
        [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<svg xmlns="http://www.w3.org/2000/svg" width="320" height="120" viewBox="0 0 320 120">',
            '<rect width="100%" height="100%" fill="#fafafa"/>',
            f'<text x="160" y="60" text-anchor="middle" font-size="12" fill="#666">{escape(msg)}</text>',
            "</svg>",
        ]
    )
