from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, RichLog, Static, Tabs, TabbedContent, TabPane, Label
from textual.containers import Horizontal, Vertical
from textual import events
from map_widget import MapWidget
from engine import Engine
from gamemap import GameMap
from entity import Entity
from datetime import datetime
from rich.text import Text


class StatsPane(Static):
    def __init__(self, player: Entity):
        super().__init__()
        self.player = player
        
    def render(self) -> Text:
        return Text(
            f"Player Stats:\n"
            f"Name: {self.player.name}\n"
            f"Position: ({self.player.x}, {self.player.y})\n"
            f"Health: 100\n"  # Replace with actual player health if available
            f"Strength: 10"   # Replace with actual player stats if available
        )


class InventoryPane(Static):
    def __init__(self, items: list[str]):
        super().__init__()
        self.items = items

    def render(self) -> Text:
        return Text("Inventory:\n" + "\n".join(self.items or ["Empty"]))

class RoguelikeApp(App):
    CSS_PATH = "ui/styles.tcss"
    CSS = """
    Horizontal {
        layout: horizontal;
        height: 100%;
    }
    .left-panel {
        width: 3fr;
    }
    .right-panel {
        width: 1fr;
    }
    MapWidget {
        height: 3fr;
        padding: 1;
    }
    RichLog {
        height: 1fr;
        border: round green;
        background: #111111;
        color: white;
        padding: 1;        
    }
    TabbedContent {
        height: 100%;
        border: round green;
        background: #111111;
        color: #00ff00;
        padding: 1;
    }
    """

    """
    BINDINGS = [
        ("s", "show_tab('stats')", "Show Stats Tab"),
        ("i", "show_tab('inventory')", "Show Inventory Tab"),
    ]
    """
    def compose(self) -> ComposeResult:
        game_map = GameMap(120, 30)
        game_map.generate_dungeon()
        player = Entity(x=20, y=8, char='@', name='Player', color='green')
        enemy = Entity(x=15, y=11, char='E', name='Enemy', color='red')
        engine = Engine(game_map, player)
        engine.add_entity(enemy)
        self.inventory = ["Sword", "Shield"]  # Example inventory

        yield Header(show_clock=True)
        with Horizontal():
            with Vertical(classes="left-panel"):
                yield MapWidget(engine)
                yield RichLog(highlight=True, markup=True, wrap=True, id="action-log")
            with Vertical(classes="right-panel"):
                with TabbedContent():
                    with TabPane("Stats", id="StatsPane"):
                        yield StatsPane(player)
                    with TabPane("Inventory", id="InventoryPane"):
                        yield InventoryPane(self.inventory)

        yield Footer()

    def log_action(self, kind: str, message: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        color = {
            "movement": "green",
            "combat": "red",
            "loot": "yellow",
            "mouse": "cyan",
            "click": "magenta",
        }.get(kind, "white")
        formatted = f"[dim]{timestamp}[/dim] [bold {color}]{message}[/bold {color}]"
        self.query_one(RichLog).write(formatted)


    def on_mouse_move(self, event: events.MouseMove) -> None:
        pass
        """
        test = f"{event.widget}"
        if test == 'MapWidget()':
            if event.get_content_offset(event.widget):
                x, y = event.get_content_offset(event.widget)
                self.log_action("mouse", f"mouse at ({x}, {y}) - offset {event.get_content_offset(event.widget)}")
        """

    def on_click(self, event: events.Click) -> None:
        if event.get_content_offset(event.widget):
            x, y = event.get_content_offset(event.widget)
            self.log_action("click", f"mouse clicked at ({x}, {y})")


    def update_stats(self) -> None:
        """Update the Stats tab content."""
        stats_pane = self.query_one(StatsPane)
        stats_pane.refresh()

    def update_inventory(self, new_items: list[str]) -> None:
        """Update the Inventory tab content with new items."""
        self.inventory = new_items
        inventory_pane = self.query_one(InventoryPane)
        inventory_pane.items = new_items
        inventory_pane.refresh()

    def action_show_tab(self, tab: str) -> None:
        """Switch to a new tab."""
        self.get_child_by_type(TabbedContent).active = tab

    @property
    def items(self) -> list[str]:
        """Getter for inventory items."""
        return self.inventory

if __name__ == "__main__":
    RoguelikeApp().run()
