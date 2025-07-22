from gamemap import GameMap
from entity import Entity


class Engine:
    def __init__(self, game_map: GameMap, player: Entity):
        self.game_map = game_map
        self.player = player
        self.entities: list[Entity] = [player]

    def add_entity(self, entity: Entity):
        self.entities.append(entity)

    def handle_input(self, key: str) -> bool:
        dx, dy = 0, 0
        if key in ("w", "up"):
            dy = -1
        elif key in ("s", "down"):
            dy = 1
        elif key in ("a", "left"):
            dx = -1
        elif key in ("d", "right"):
            dx = 1
        elif key == "escape":
            return False

        dest_x = self.player.x + dx
        dest_y = self.player.y + dy

        if self.game_map.is_walkable(dest_x, dest_y):
            self.player.move(dx, dy)
            return "moved"
        else:
            return "blocked"

        return True
