from typing import Optional
#part of Python's type hinting system. Optional denotes something that could be set to None.

import tcod.event
#we don't need to import the entirety of tcod. we only need the contents of tcod.event here.

from actions import Action, EscapeAction, MovementAction
#importing Action class and the subclasses we created in actions.py.

class EventHandler(tcod.event.EventDispatch[Action]):
    # creating a subclass of tcod's EventDispatch class. 
    # EventDispatch lets us send an event to its proper method based on the type of event.
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()
    #ev_quit is a method from EventDispatch. It's called when you click the X in the window of the program.    

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        #this method receives key press events and returns an Action subclass or None (if no valid key was pressed).
        action: Optional[Action] = None

        key = event.sym
        #action will hold whatever subclass of Action we end up assigning. It will stay on None if we don't find any valid key.
        #key holds the key we have pressed, but doesn't contain any additional information about modifiers like Shift or Alt.

        if key == tcod.event.K_UP:
            action = MovementAction(dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = MovementAction(dx=0, dy=1)
        elif key == tcod.event.K_LEFT:
            action = MovementAction(dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT:
            action = MovementAction(dx=1, dy=0)

        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()

        # No valid key pressed:
        return action

        #now that we have decided what action is taking place (or if no action is taking place), we return it.