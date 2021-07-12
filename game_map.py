import numpy as np #type: ignore
from tcod.console import Console

import tile_types

class GameMap:
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")
# initializer takes width and height, assigning them in one line.
# self.tiles creates a 2D array all filled with the same values: in this case, all WALLS.
# now in part 3: we are filling with walls, and carving out rooms with floors using a dungeon generator.


    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height
    #method turns true if x/y are within map boundaries. ensures player stays in bounds. 

    def render(self, console: Console) -> None:
        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles["dark"]

    #we can quickly render the whole map with console.tiles_rgb. should be much faster than console.print