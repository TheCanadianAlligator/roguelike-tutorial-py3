#!/usr/bin/env python3
import tcod

#from actions import EscapeAction, MovementAction #well, not anymore
from engine import Engine
from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler
#importing classes from other files

def main() -> None:
    screen_width = 80
    screen_height = 50
# screen size variables

    map_width  = 80
    map_height = 45

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

    game_map = GameMap(map_width, map_height)

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
            
            #root_console.print(x=player.x, y=player.y, string=player.char, fg=player.color)    
            #telling the program to put the player at their base position.
            #if removing this breaks things, uncomment this! seems ok for now...

            engine.render(console=root_console, context=context)

            events = tcod.event.wait()

            engine.handle_events(events)
            
            #context.present(root_console)       #context.present updates the screen

            # root_console.clear() #clears the console after we've drawn it, so we don't get "ghosts" hanging around after something moves.

            # for event in tcod.event.wait(): #wait for input from user, loops through each event that happens

            #     action = event_handler.dispatch(event)
            #     #the event is sent to event_handler's dispatch method, which sends the event to its proper place.

            #     if action is None:
            #         continue
                
            #     if isinstance(action, MovementAction):
            #         player.move(dx=action.dx, dy=action.dy)

            #     # pulls the dx and dy from input_handlers MovementAction, and modifies the player's position (player_x and y) accordingly. 
            #     # dx/dy should only ever be -1, 0, or 1 for now.

            #     elif isinstance(action, EscapeAction):
            #         raise SystemExit()

    # This doesn't need to be here anymore! engine.py is handling this all now. Commented here so we can compare what's been moved to engine in part 2.


if __name__ == "__main__":
    main()
# only runs the main() function when we go to the terminal and run "python engine.py"
# https://stackoverflow.com/questions/419163/what-does-if-name-main-do/419185#419185

