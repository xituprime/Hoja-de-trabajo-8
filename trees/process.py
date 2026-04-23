class Process:
    def __init__(self, pid: int, vruntime: float) -> None:
        self.pid: int = pid
        self.vruntime: float = vruntime

    def __repr__(self) -> str:
        return f"Process(pid={self.pid}, vruntime={self.vruntime:.2f})"
