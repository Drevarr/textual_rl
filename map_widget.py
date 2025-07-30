from textual.widgets import Static
from rich.text import Text
from textual import events
from engine import Engine


class MapWidget(Static):
    def __init__(self, engine: Engine):
        super().__init__()
        self.engine = engine
        self.can_focus = True
        self.viewport_width = 80
        self.viewport_height = 20

    def on_mount(self) -> None:
        self.focus()

    def on_key(self, event: events.Key) -> None:
        key = event.key
        result = self.engine.handle_input(key)

        if result == "exit":
            self.app.exit()
            return

        self.refresh()

        if result == "moved":
            self.app.log_action(
                "movement",
                f"{self.engine.player.name} moved to ({self.engine.player.x}, {self.engine.player.y})"
            )
        elif result == "blocked":
            self.app.log_action(
                "blocked",
                f"{self.engine.player.name} bumps into a wall!"
            )

    def get_viewport_bounds(self) -> tuple[int, int, int, int]:
        px, py = self.engine.player.x, self.engine.player.y
        w, h = self.viewport_width, self.viewport_height
        gm = self.engine.game_map

        half_w = w // 2
        half_h = h // 2

        # Clamp viewport to map bounds
        x0 = max(0, min(px - half_w, gm.width - w))
        y0 = max(0, min(py - half_h, gm.height - h))
        x1 = x0 + w
        y1 = y0 + h

        return x0, y0, x1, y1


    def render(self) -> Text:
        text = Text()
        gm = self.engine.game_map
        x0, y0, x1, y1 = self.get_viewport_bounds()
        px, py = self.engine.player.x, self.engine.player.y
        rendered_rows = gm.render()

        for y in range(y0, y1):
            for x in range(x0, x1):
                entity = next(
                    (e for e in self.engine.entities if e.x == x and e.y == y),
                    None,
                )

                if gm.is_visible(x, y):
                    if entity:
                        text.append(entity.char, style=entity.color)
                    else:
                        dist = gm.player_distance(x, y, px, py)
                        if dist <= 2:
                            style = "#CC7621"
                        elif dist <= 4:
                            style = "#804A15"
                        elif dist <= 6:
                            style = "#4C2C0C"
                        else:
                            style = "#190F04"                        

                        char = rendered_rows[y][x]
                        text.append(char, style=style)

                elif gm.is_explored(x, y):
                    if entity:
                        text.append(entity.char, style="grey37")
                    else:
                        char = gm.render()[y][x]
                        if char == "·":
                            text.append(char, style="grey23")
                        elif char == "▒":
                            text.append(char, style="grey30")
                        else:
                            text.append(char, style="grey27")
                else:
                    text.append(" ")

            text.append("\n")

        return text
