from typing import Set, Iterable, Any
from tcod.constants import FOV_BASIC

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov        #PART 4 addition

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
        self.update_fov()

    # entities is a Set[Entity], sort of like a list that enforces uniqueness. An Entity can't be added to the set twice - a list would allow that.
    # event_handler is the same as in main.py.
    # player is the player Entity. We will be accessing this a lot, so we want to have it outside of the set.

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)

            self.update_fov() #Update the FOV before the player's next action.

    def update_fov(self) -> None:
        """Recompute the visible area based on the player's point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"], #considers any non-zero values to be transparent, calculating the field of view.
            (self.player.x, self.player.y),     #this is where the game's POV is, where things will be marked as "visible." we are putting it on the player's x/y.
            radius=8,
        )
        # If a tile is "visible" it should be added to "explored."
        self.game_map.explored |= self.game_map.visible         # |= is a bitwise OR operator, this adds the explored tile to the visible array while carrying over things like flags. https://stackoverflow.com/questions/14295469/what-does-mean-pipe-equal-operator

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        for entity in self.entities:
            #console.print(entity.x, entity.y, entity.char, fg=entity.color)
            #NOW IN PART 4: ONLY printing entities in the FOV!
            if self.game_map.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)

        console.clear()

        # draws the screen. iterate through self.entities and prints them to their proper locations, presents the context, and clears the console, like in main.py.
