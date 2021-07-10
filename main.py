#!/usr/bin/env python3
import tcod

from actions import EscapeAction, MovementAction
from input_handlers import EventHandler
#importing classes from actions.py and input_handlers.py

def main() -> None:
    screen_width = 80
    screen_height = 50
# screen size variables

    player_x = int(screen_width/2)
    player_y = int(screen_height/2)

    #placing the player automatically in the middle

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )
# telling tcod what tileset to use - the 10x10 tileset in the project folder.

    event_handler = EventHandler()
    # an instance of our EventHandler class. recieves and processes events.

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial", #the heading bar. rename this when you figure out what you're gonna call the game. or don't!
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F") #numpy, by default, accesses 2d arrays in [y,x] order; setting order="F" lets us change this to [x,y]
        while True:     #the game loop. this will never end until we close the screen.
            
            # root_console.print(x=1, y=1, string="@")    #telling the program to put @ at x=1, y=1
            root_console.print(x=player_x, y=player_y, string = "@")    #telling the program to put the @ at the base character position

            context.present(root_console)       #context.present updates the screen

            root_console.clear() #clears the console after we've drawn it, so we don't get "ghosts" hanging around after something moves.

            for event in tcod.event.wait(): #wait for input from user, loops through each event that happens
                # if event.type == "QUIT":
                #     raise SystemExit()

                #lets the game gracefully exit without crashing, by hitting the x button at the top of the window.

                action = event_handler.dispatch(event)
                #the event is sent to event_handler's dispatch method, which sends the event to its proper place.

                if action is None:
                    continue
                
                if isinstance(action, MovementAction):
                    player_x += action.dx
                    player_y += action.dy

                # pulls the dx and dy from input_handlers MovementAction, and modifies the player's position (player_x and y) accordingly. 
                # dx/dy should only ever be -1, 0, or 1 for now.

                elif isinstance(action, EscapeAction):
                    raise SystemExit()



if __name__ == "__main__":
    main()
# only runs the main() function when we go to the terminal and run "python engine.py"
# https://stackoverflow.com/questions/419163/what-does-if-name-main-do/419185#419185

