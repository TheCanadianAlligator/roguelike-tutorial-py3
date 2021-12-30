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

# now in part 4: we are adding self.visible and self.explored to differentiate tiles we can see right now, and ones we have seen before.
        
        self.visible = np.full((width, height), fill_value=False, order="F")    #tiles we can see right now.
        self.explored = np.full((width, height), fill_value=False, order="F")   #tiles we have seen before.


    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height
    #method turns true if x/y are within map boundaries. ensures player stays in bounds. 

    def render(self, console: Console) -> None:

        # In part 4 we added a new rendering method to implement the light/dark/shroud tiles behaviour.
        """Renders the map.
        
        If a tile is in the "visible" array, then draw it with "light" colors.
        If it isn't, but it's in the "explored" array, then draw it with the "dark" colors.
        Otherwise, the defualt is "SHROUD."
        """
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(     #np.select lets us conditionally draw the tiles we want based on what is in condlist.
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles['dark']],
            default=tile_types.SHROUD       #if no conditions are met, draw with SHROUD.
        )

    #we can quickly render the whole map with console.tiles_rgb. should be much faster than console.print