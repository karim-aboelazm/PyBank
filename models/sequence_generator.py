class SequenceGenerator:
    def __init__(self, prefix: str, start: int = 1):
        self.prefix = prefix
        self.counter = start

    def next_id(self) -> str:
        value = f"{self.prefix}{self.counter:05d}"
        self.counter += 1
        return value