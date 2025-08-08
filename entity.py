from dataclasses import dataclass


@dataclass
class Entity:
    x: int
    y: int
    facing = (1, 0)  # Facing right by default
    char: str
    name: str
    color: str = "green"
    max_hp: int = 100
    hitpoints: int = 100
    strength: int = 18

    def move(self, dx: int, dy: int):
        self.x += dx
        self.y += dy
        self.facing = (dx, dy) if (dx, dy) != (0, 0) else self.facing

