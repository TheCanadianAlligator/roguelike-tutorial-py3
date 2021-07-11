from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console

#from actions import EscapeAction, MovementAction
from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler


class Engine:
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, game_map: GameMap, player: Entity):
        self.entities = entities
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player

    # entities is a Set[Entity], sort of like a list that enforces uniqueness. An Entity can't be added to the set twice - a list would allow that.
    # event_handler is the same as in main.py.
    # player is the player Entity. We will be accessing this a lot, so we want to have it outside of the set.

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)

            # this can now be simplified with new developments in actions

            # if isinstance(action, MovementAction):
            #     if self.game_map.tiles["walkable"][self.player.x + action.dx, self.player.y + action.dy]:
            #         self.player.move(dx=action.dx, dy=action.dy)

            # elif isinstance(action, EscapeAction):
            #     raise SystemExit()

        # very similar to event processing in main.py in part 1! events pass through to this to be interated, and self.event_handler will handle them.

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)

        console.clear()

        # draws the screen. iterate through self.entities and prints them to their proper locations, presents the context, and clears the console, like in main.py.
