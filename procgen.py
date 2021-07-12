from __future__ import annotations

import random

from typing import Iterator, List, Tuple, TYPE_CHECKING

import tcod

from game_map import GameMap
import tile_types

if TYPE_CHECKING:
    from entity import Entity

class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
    
    #takes the x/y coords of the top left, and computes the bottom right based on width and height

    @property
    def center(self) -> Tuple[int,int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    #center is a property, like a read-only variable for RectangularRoom class.
    #describes the x/y coordinates of the center of a room.

    @property
    def inner(self) -> Tuple[slice,slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1+1, self.y2)

    #inner property returns 2 slices, representing the inner portion of the room.
    #this is the part we are digging out for our room in the dungeon generator.
    #the inner part of the room is at +1, because lists are 0-indexed: 
    #the walls would take up anything living on the 0 lines

    def intersects(self, other: RectangularRoom) -> bool:
        """Return True if this room overlaps with another RectangularRoom."""
        return(
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )
    
    #checks if the room and another room intersect or not. determines if two rooms are overlapping.

def tunnel_between(
    start: Tuple[int,int], end: Tuple[int,int]
) -> Iterator[Tuple[int,int]]:
    """Return an L-shaped tunnel between these two points."""
    x1,y1 = start
    x2,y2 = end
    if random.random() < 0.5:   #50% chance.
        #move horizontal, then vertical
        corner_x, corner_y = x2, y1
    else:
        #move vertical, then horizontal
        corner_x, corner_y = x1, y2

    #Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1,y1), (corner_x,corner_y)).tolist():
        yield x,y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2,y2)).tolist():
        yield x,y
    
    #tcod line of sight module - bresenham lines function. https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
    #we use it to get a line from one point to another.
    #yield expressions return a "generator." after returning the value, it doesn't exit the function: 
    #it keeps the local state, which allows the function to pick up where it left off.

# def generate_dungeon(map_width, map_height) -> GameMap:
#     dungeon = GameMap(map_width, map_height)

#     room_1 = RectangularRoom(x=20,y=15,width=10,height=15)
#     room_2 = RectangularRoom(x=35,y=15,width=10,height=15)

#     dungeon.tiles[room_1.inner] = tile_types.floor
#     dungeon.tiles[room_2.inner] = tile_types.floor

#     for x, y in tunnel_between(room_2.center, room_1.center):
#         dungeon.tiles[x,y] = tile_types.floor

#     return dungeon

#     #sample dungeon. this isn't actually procgen yet - we're seeing if generation works at all.

def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    player: Entity,
) -> GameMap:
    """Generate a new dungeon map."""
    dungeon = GameMap(map_width, map_height)

    rooms: List[RectangularRoom] = []
    #running list of all rooms. without any rooms generated, it's empty [].

    for r in range(max_rooms): 
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height -1)

        #"RectangularRoom" class makes rectangles easier to work with.
        new_room = RectangularRoom(x, y, room_width, room_height)

        #Run through the other rooms and see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue    #this room intersects, go on to the next attempt.
        #If there are no intersections then the room is valid.
        #If a room *does* intersect, we just toss it out, using continue to skip the rest of the loop.

        #Dig out the room's inner area.
        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            #starting room.
            player.x, player.y = new_room.center
        else: #all rooms after the first.
            #dig out a tunnel between this room and the previous
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x,y] = tile_types.floor

        #append the new room to the list
        rooms.append(new_room)

    return dungeon