from typing import Tuple
#Tuples are used to store multiple items in a single variable


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x: int, y:int, char: str, color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.char = char
        self.color = color 

    #an entity's colour is a Tuple of 3 integers, representing its rgb values.

    def move(self, dx: int, dy: int) -> None:
        #move the entity by a given amount
        self.x += dx
        self.y += dy