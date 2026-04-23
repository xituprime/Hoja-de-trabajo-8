# Hoja de Trabajo 8 — Árboles y Sistemas Operativos

> Simulación y comparación de estructuras de árboles de búsqueda aplicadas a la planificación de procesos de un sistema operativo.

## Integrantes

- Franco Paiz 25780
- Axel Xitumul

---

## Propósito

En sistemas operativos modernos como Linux, el **Completely Fair Scheduler (CFS)** no gestiona los procesos en una cola FIFO simple. En cambio, asigna a cada proceso un tiempo de ejecución virtual (`vruntime`) y utiliza un árbol para encontrar siempre el proceso con el menor `vruntime` de forma eficiente.

Este proyecto simula ese comportamiento comparando dos estructuras de datos:

| Estructura | Característica clave |
|---|---|
| **BST** (Binary Search Tree) | Simple, sin balanceo. O(log n) promedio, O(n) peor caso. |
| **Splay Tree** | Auto-ajustable. Accesos frecuentes al mismo nodo se vuelven O(1). |

El objetivo es entender empíricamente el comportamiento de estas estructuras en escenarios típicos de planificación.

---

## Estructura del proyecto

```
HT8-Trees/
├── trees/
│   ├── abstract_tree.py     # Clase base abstracta (ABC)
│   ├── node.py              # Nodo genérico (compatible con BST y Splay)
│   ├── process.py           # Modelo de proceso con pid y vruntime
│   ├── bst.py               # Árbol Binario de Búsqueda estándar
│   └── splay.py             # Splay Tree con rotaciones
├── simulations/
    └── main.py                  # Script principal con los 3 escenarios
├── docs/
│   └── uml_ht8.png          # Diagrama UML
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
Se insertan 1 000 procesos con `vruntime` aleatorio en los dos árboles. Se buscan 100 procesos al azar y se promedian las iteraciones. Se contrasta con la complejidad teórica O(log n).

### Escenario B — Llegada secuencial (peor caso)
Se insertan 1 000 procesos en orden ascendente (1, 2, 3 … 1000). Se busca el proceso 1000. El BST degenera en una lista enlazada (999 pasos), mientras el Splay Tree puede reestructurarse según los accesos.

### Escenario C — Proceso frecuente de I/O
Se simula un proceso que regresa constantemente al estado `ready` (I/O frecuente). Se busca el mismo proceso 50 veces seguidas. El Splay Tree lo mueve a la raíz en la primera búsqueda, reduciendo las siguientes a 0 pasos.

---

## Resultados

| Escenario | BST | Splay Tree |
|---|---|---|
| A — promedio 100 búsquedas aleatorias | ~11 pasos | ~11 pasos |
| B — buscar proceso 1000 (ordenado) | **999 pasos** | ~0 pasos |
| C — mismo proceso 50 veces | N/A | **~0.24 promedio** |

---


## Referencias

- [The Linux Kernel Documentation — CFS Scheduler](https://www.kernel.org/doc/html/latest/scheduler/sched-design-CFS.html)
- [Introduction to Algorithms — Cormen et al. (CLRS)](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/)
