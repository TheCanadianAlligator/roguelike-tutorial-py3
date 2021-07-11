from typing import Tuple

import numpy as np #type: ignore

#Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = np.dtype(
    [
        ("ch", np.int32), #Unicode codepoint.
        ("fg", "3B"),   # 3 unsigned bytes, for RGB.
        ("bg", "3B"),
    ]
)

#dtype is a datatype that numpy can use. it's made up of 3 parts:
#ch is the character, represented in integer format. we'll translate from Unicode integer.
#fg is the foreground colour. 3B means 3 unsigned bytes, whhich can be used for RGB color codes.
#bg is the background colour, similar to fg.


#Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", np.bool), #True if this tile can be walked over.
        ("transparent", np.bool),   #True if this tile doesn't block FOV.
        ("dark", graphic_dt),   #Graphics for when this tile is not in FOV.
    ]
)
# dark uses graphic_dt, the dtype we just defined above. remember: graphic_dt holds the character, background, and foreground colour. 
# we'll be working with this later.

def new_tile(
    *, #enforce the use of keywords, so paramater order doesn't matter.
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
)   -> np.ndarray:
    """Helper function for defining individual tile types"""
    return np.array((walkable, transparent, dark), dtype=tile_dt)

# helper function used to define file types. takes parameters and creates a numpy array of just one tile_dt element.

floor = new_tile(
    walkable=True, transparent=True, dark=(ord("."), (255,255,255), (50,50,150)),
)
wall = new_tile(
    walkable=False, transparent=False, dark=(ord("#"), (255,255,255), (0,0,100)),
)
#tile types! i think ord is supposed to the be space character? foreground is next, followed by background.