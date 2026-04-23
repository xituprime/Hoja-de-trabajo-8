import random
import os
from typing import List, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from trees.process import Process
from trees.bst import BinarySearchTree
from trees.splay import SplayTree
from trees.rbt import RedBlackTree

# Helpers

def generateProcesses(n: int, ordered: bool = False) -> List[Process]:
    """
    Genera n procesos.
    Si ordered=True, los vruntime son 1..n (caso peor para BST).
    Si ordered=False, son flotantes aleatorios en [0, 100_000).
    """
    if ordered:
        return [Process(pid=i, vruntime=float(i)) for i in range(1, n + 1)]
    
    vruntimes = random.sample(range(1, 10_000_000), n)   # sin duplicados
    return [Process(pid=i, vruntime=float(v)) for i, v in enumerate(vruntimes, 1)]


def buildTree(tree_class, processes: List[Process]):
    """Construye un árbol insertando todos los procesos."""
    tree = tree_class()
    for p in processes:
        tree.insert(p)
    return tree


def searchMany(tree, vruntimes: List[float]) -> List[int]:
    """Retorna la lista de pasos para cada búsqueda."""
    results = []
    for v in vruntimes:
        _, steps = tree.search(v)
        results.append(steps)
    return results


def saveBarChart(title: str, xlabel: str, ylabel: str,
                 labels: List[str], values: List[float],
                 colors: List[str], filename: str,
                 extra_info: str = "") -> None:
    """Genera y guarda un gráfico de barras comparativo."""
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(labels, values, color=colors, edgecolor="black", width=0.5)

    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.3,
                f"{val:.2f}", ha="center", va="bottom", fontsize=11, fontweight="bold")

    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_ylim(0, max(values) * 1.25 + 1)
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    if extra_info:
        fig.text(0.5, -0.04, extra_info, ha="center", fontsize=9, style="italic")

    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  → Gráfica guardada: {filename}")


# ─────────────────────────────────────────────
# Scenario A — Random Arrival
# ─────────────────────────────────────────────

def runScenarioA() -> None:
    print("\n" + "=" * 60)
    print("ESCENARIO A — Llegada Aleatoria (1 000 procesos)")
    print("=" * 60)

    N = 1000
    SAMPLE = 100
    processes = generateProcesses(N, ordered=False)

    bst   = buildTree(BinarySearchTree, processes)
    splay = buildTree(SplayTree, processes)
    rbt   = buildTree(RedBlackTree, processes)

    # Seleccionar 100 procesos que ya están en el árbol
    sample_procs = random.sample(processes, SAMPLE)
    sample_vr = [p.vruntime for p in sample_procs]

    bst_steps   = searchMany(bst,   sample_vr)
    splay_steps = searchMany(splay, sample_vr)
    rbt_steps   = searchMany(rbt,   sample_vr)

    avg_bst   = sum(bst_steps)   / SAMPLE
    avg_splay = sum(splay_steps) / SAMPLE
    avg_rbt   = sum(rbt_steps)   / SAMPLE

    import math
    log2_n = math.log2(N)

    print(f"  Promedio BST:          {avg_bst:.2f} pasos")
    print(f"  Promedio Splay Tree:   {avg_splay:.2f} pasos")
    print(f"  Promedio Red-Black:    {avg_rbt:.2f} pasos")
    print(f"  Referencia O(log n):   {log2_n:.2f} pasos  (log₂ {N})")

    saveBarChart(
        title="Escenario A — Promedio de pasos en búsqueda (entrada aleatoria)",
        xlabel="Estructura de datos",
        ylabel="Promedio de pasos",
        labels=["BST", "Splay Tree", "Red-Black Tree"],
        values=[avg_bst, avg_splay, avg_rbt],
        colors=["#4C72B0", "#DD8452", "#55A868"],
        filename="output/scenario_a_avg_steps.png",
        extra_info=f"n={N} procesos | 100 búsquedas aleatorias | O(log n) ≈ {log2_n:.1f}"
    )

    # Gráfica de dispersión: índice de búsqueda vs pasos
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(range(SAMPLE), bst_steps,   "o-", color="#4C72B0", label="BST",   alpha=0.7, markersize=4)
    ax.plot(range(SAMPLE), splay_steps, "s-", color="#DD8452", label="Splay", alpha=0.7, markersize=4)
    ax.plot(range(SAMPLE), rbt_steps,   "^-", color="#55A868", label="RBT",   alpha=0.7, markersize=4)
    ax.axhline(y=log2_n, color="red", linestyle="--", label=f"O(log n)≈{log2_n:.1f}")
    ax.set_title("Escenario A — Pasos por búsqueda individual", fontsize=12, fontweight="bold")
    ax.set_xlabel("Índice de búsqueda")
    ax.set_ylabel("Pasos")
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("output/scenario_a_per_search.png", dpi=150)
    plt.close()
    print("  → Gráfica guardada: output/scenario_a_per_search.png")

    return avg_bst, avg_splay, avg_rbt


# Main

def main() -> None:
    random.seed(42)  # Reproducibilidad
    os.makedirs("output", exist_ok=True)

    print("╔══════════════════════════════════════════════════════════╗")
    print("║  Hoja de Trabajo 8 — Árboles y Sistemas Operativos      ║")
    print("║  BST vs Splay Tree vs Red-Black Tree                     ║")
    print("╚══════════════════════════════════════════════════════════╝")

    avg_bst_a, avg_splay_a, avg_rbt_a = runScenarioA()
    

    print("\n" + "=" * 60)
    print("RESUMEN FINAL")
    print("=" * 60)
    print(f"{'Escenario':<35} {'BST':>10} {'Splay':>10} {'RBT':>10}")
    print("-" * 65)
    print(f"{'A — promedio (100 búsquedas aleatorias)':<35} "
          f"{avg_bst_a:>10.2f} {avg_splay_a:>10.2f} {avg_rbt_a:>10.2f}")

    print("\nTodas las gráficas guardadas en la carpeta output/")


if __name__ == "__main__":
    main()