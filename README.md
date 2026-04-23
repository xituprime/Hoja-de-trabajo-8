# Hoja de Trabajo 8 — Árboles y Sistemas Operativos

> Simulación y comparación de estructuras de árboles de búsqueda aplicadas a la planificación de procesos de un sistema operativo.

## Integrantes

- Franco Paiz 25780
- Axel Xitumul

---

## Propósito

En sistemas operativos modernos como Linux, el **Completely Fair Scheduler (CFS)** no gestiona los procesos en una cola FIFO simple. En cambio, asigna a cada proceso un tiempo de ejecución virtual (`vruntime`) y utiliza un árbol para encontrar siempre el proceso con el menor `vruntime` de forma eficiente.

Este proyecto simula ese comportamiento comparando tres estructuras de datos:

| Estructura | Característica clave |
|---|---|
| **BST** (Binary Search Tree) | Simple, sin balanceo. O(log n) promedio, O(n) peor caso. |
| **Splay Tree** | Auto-ajustable. Accesos frecuentes al mismo nodo se vuelven O(1). |
| **Red-Black Tree** | Balanceo estricto garantizado. O(log n) en todos los casos. |

El objetivo es entender empíricamente por qué el kernel de Linux eligió el Red-Black Tree para el CFS.

---

## Estructura del proyecto

```
HT8-Trees/
├── trees/
│   ├── __init__.py          # Exporta todas las clases
│   ├── abstract_tree.py     # Clase base abstracta (ABC)
│   ├── node.py              # Nodo genérico (compatible con BST, Splay y RBT)
│   ├── process.py           # Modelo de proceso con pid y vruntime
│   ├── bst.py               # Árbol Binario de Búsqueda estándar
│   ├── splay.py             # Splay Tree con rotaciones Zig/Zig-Zig/Zig-Zag
│   └── rbt.py               # Red-Black Tree con fix-up y nodo NIL sentinel
├── simulations/
    └── main.py                  # Script principal con los 3 escenarios
├── docs/
│   └── uml_ht8.xml          # Diagrama UML (importable en draw.io)
├── output/                  # Gráficas generadas automáticamente
└── README.md
```

---

## Cómo ejecutar

### Requisitos

- Python 3.10 o superior
- matplotlib

```bash
pip install matplotlib
```

### Ejecución

```bash
python main.py
```

Las gráficas se guardan automáticamente en la carpeta `output/`.

---

## Escenarios simulados

### Escenario A — Llegada aleatoria
Se insertan 1 000 procesos con `vruntime` aleatorio en los tres árboles. Se buscan 100 procesos al azar y se promedian las iteraciones. Se contrasta con la complejidad teórica O(log n).

### Escenario B — Llegada secuencial (peor caso)
Se insertan 1 000 procesos en orden ascendente (1, 2, 3 … 1000). Se busca el proceso 1000. El BST degenera en una lista enlazada (999 pasos), mientras el RBT mantiene O(log n).

### Escenario C — Proceso frecuente de I/O
Se simula un proceso que regresa constantemente al estado `ready` (I/O frecuente). Se busca el mismo proceso 50 veces seguidas. El Splay Tree lo mueve a la raíz en la primera búsqueda, reduciendo las siguientes a 0 pasos.

---

## Resultados

| Escenario | BST | Splay Tree | Red-Black Tree |
|---|---|---|---|
| A — promedio 100 búsquedas aleatorias | ~11 pasos | ~11 pasos | ~8 pasos |
| B — buscar proceso 1000 (ordenado) | **999 pasos** | ~0 pasos | ~16 pasos |
| C — mismo proceso 50 veces | N/A | **~0.24 promedio** | ~8 constante |

---


## Referencias

- [The Linux Kernel Documentation — CFS Scheduler](https://www.kernel.org/doc/html/latest/scheduler/sched-design-CFS.html)
- [Introduction to Algorithms — Cormen et al. (CLRS)](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/)
