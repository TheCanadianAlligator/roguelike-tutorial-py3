class Action: 
    pass

# This is the main class, Action. We are going to have other subclasses under it, defining what kind of Action has taken place.

class EscapeAction(Action):
    pass

# EscapeAction will be for when we hit the Esc key.

class MovementAction(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()  #super() returns a temporary object of the superclass that lets us call the superclass' methods
        self.dx = dx
        self.dy = dy

# MovementAction is for describing when we move our player around. 
# We are giving it the dx and dy arguments because we will need to know that we are not only moving, but also moving in a direction.

