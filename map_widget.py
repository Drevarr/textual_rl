from textual.widgets import Static
from rich.text import Text
from textual import events
from engine import Engine


class MapWidget(Static):
    def __init__(self, engine: Engine):
        super().__init__()
        self.engine = engine
        self.can_focus = True

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


    def render(self) -> Text:
        text = Text()
        gm = self.engine.game_map
        # Get the map's string representation from GameMap.render()
        map_rows = gm.render()

        for y, row in enumerate(map_rows):
            for x, char in enumerate(row):
                # Check if there's an entity at this position
                entity = next((e for e in self.engine.entities if e.x == x and e.y == y), None)
                if entity:
                    # Render entity character with its color
                    text.append(entity.char, style=entity.color)
                else:
                    # Render map tile ('.' for floor, '#' for wall)
                    style = "white" if char == "." else "grey50"
                    text.append(char, style=style)
            text.append("\n")

        return text

