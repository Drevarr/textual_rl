from dataclasses import dataclass


@dataclass
class Entity:
    x: int
    y: int
    char: str
    name: str
    color: str = "white"

    def move(self, dx: int, dy: int):
        self.x += dx
        self.y += dy
