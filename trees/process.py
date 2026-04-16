class Process:
    def __init__(self, pid: int, vruntime: float) -> None:
        self.pid: int = pid
        self.vruntime: float = vruntime

