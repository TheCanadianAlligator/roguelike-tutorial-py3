#!/usr/bin/env python3
import tcod

from engine import Engine
from entity import Entity
# from game_map import GameMap
from input_handlers import EventHandler
from procgen import generate_dungeon
#importing classes from other files

def main() -> None:
    screen_width = 80
    screen_height = 50
# screen size variables

    map_width  = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )
# telling tcod what tileset to use - the 10x10 tileset in the project folder.

    event_handler = EventHandler()
    # an instance of our EventHandler class. recieves and processes events.

    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", (255,255,255))
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), "@", (255,255,0))
    entities = {npc, player}

    # New with entities: still putting our player in the middle of the screen, and giving them a friend. 
    # Both will be represented by @, but differently coloured.

    # game_map = GameMap(map_width, map_height)
    game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        player=player
    )

    engine = Engine(entities=entities, event_handler=event_handler, game_map=game_map, player=player)

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial", #the heading bar. rename this when you figure out what you're gonna call the game. or don't!
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F") #numpy, by default, accesses 2d arrays in [y,x] order; setting order="F" lets us change this to [x,y]
        while True:     #the game loop. this will never end until we close the screen.

            engine.render(console=root_console, context=context)

            events = tcod.event.wait()

            engine.handle_events(events)


if __name__ == "__main__":
    main()
# only runs the main() function when we go to the terminal and run "python engine.py"
# https://stackoverflow.com/questions/419163/what-does-if-name-main-do/419185#419185

