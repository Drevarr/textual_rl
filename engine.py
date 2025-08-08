from gamemap import GameMap
from entity import Entity


class Engine:
    def __init__(self, game_map: GameMap, player: Entity):
        self.game_map = game_map
        self.player = player
        #self.entities: list[Entity] = [player]

        self.update_visibility()

    #def add_entity(self, entity: Entity):
        #self.entities.append(entity)

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
            self.update_visibility() 
            return "moved"
        else:
            return "blocked"

        return True

    def update_visibility(self):
        """Update the visible and explored tiles based on the player's current position."""
        self.game_map.compute_fov(self.player.x, self.player.y, radius=8)