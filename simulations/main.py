import random
import sys
from pathlib import Path

import matplotlib.pyplot as plt

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from trees.bst import BinarySearchTree
from trees.process import Process
from trees.splay import SplayTree


def generateProcesses(n: int) -> list[Process]:
    processes: list[Process] = []
    for i in range(n):
        pid = i + 1
        vruntime = random.uniform(0.0, 10_000.0)
        processes.append(Process(pid, vruntime))
    return processes


def runScenarioA() -> None:
    processes = generateProcesses(1000)

    bst = BinarySearchTree()
    splay = SplayTree()

    for p in processes:
        bst.insert(p)
        splay.insert(p)

    selected = random.sample(processes, 100)

    bst_steps: list[int] = []
    splay_steps: list[int] = []

    for p in selected:
        _, b_steps = bst.search(p.vruntime)
        _, s_steps = splay.search(p.vruntime)
        bst_steps.append(b_steps)
        splay_steps.append(s_steps)

    search_indices = list(range(1, len(bst_steps) + 1))

    plt.figure()
    plt.plot(search_indices, bst_steps, label="BST")
    plt.plot(search_indices, splay_steps, label="Splay")
    plt.xlabel("Número de búsqueda")
    plt.ylabel("Pasos (steps)")
    plt.legend()
    plt.title("Escenario A: llegada aleatoria")

    output_dir = _PROJECT_ROOT / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "scenario_a.png"
    plt.savefig(output_path)
    plt.close()

    avg_bst = sum(bst_steps) / len(bst_steps)
    avg_splay = sum(splay_steps) / len(splay_steps)
    print(f"Promedio de pasos BST: {avg_bst:.4f}")
    print(f"Promedio de pasos Splay: {avg_splay:.4f}")


def main() -> None:
    runScenarioA()


if __name__ == "__main__":
    main()
