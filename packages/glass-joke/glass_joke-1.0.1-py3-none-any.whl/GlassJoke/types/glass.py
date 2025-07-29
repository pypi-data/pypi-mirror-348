from dataclasses import dataclass

@dataclass
class Glass:
    full: bool = True

    def drink(self) -> None:
        self.full = False

    def refill(self) -> None:
        self.full = True
