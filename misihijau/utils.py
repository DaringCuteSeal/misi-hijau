# Copyright 2023 Cikitta Tjok

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Constructors and functions for a better workflow.

# Imports
import pyxel
from typing import Callable
from enum import Enum
from dataclasses import dataclass, field

# Enum Constants
class Direction(Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3

# Other Constants
ALPHA_COL = pyxel.COLOR_PURPLE
WINDOW_WIDTH = 256
WINDOW_HEIGHT = 256
MAP_WIDTH = 24 * 8
MAP_HEIGHT = 97 * 8

# Functions for Classes
# XXX remove if not needed
def tile_to_real(size: int):
    """
    Get real tile size from a tilemap scale.
    """
    return size * 8


# 1: Keyboard handling
class KeyTypes(Enum):
    BTN = 0
    BTNP = 1

@dataclass
class KeyFunc:
    """
    An object with a key and its associated function.
    """
    binding: int
    func: Callable[[], None]
    btn_type: KeyTypes = KeyTypes.BTN
    active: bool = True

class KeyListener:
    """
    A Key listener that is able to execute functions.
    """
    # TODO: group keybindings by game object so same keybindings with same name can exist.

    def __init__(self):
        self.checks: dict[str, KeyFunc] = {}
    
    def append(self, keyfunc: dict[str, KeyFunc]):
        """
        Append list of key listeners.
        """
        self.checks.update(keyfunc)

    def check(self):
        """
        Loop through key listeners and run function if key is pressed.
        """
        check = self.checks
        for k in check:
            if check[k].active:
                match(check[k].btn_type):
                    case KeyTypes.BTN:
                        if pyxel.btn(check[k].binding):
                            check[k].func()
                    case KeyTypes.BTNP:
                        if pyxel.btnp(check[k].binding):
                            check[k].func()


# 2: Sprites handling
@dataclass
class Coordinate:
    # XXX might be useless.
    x: int = 0
    y: int = 0
    x_map: int = 0
    y_map: int = 0

def default_costumes():
    return {}

@dataclass
class Sprite:
    """
    A sprite class with some predefined functions to make costume handling easier.
    """
    coord: Coordinate
    img: int = 0
    u: int = 0
    v: int = 0
    w: int = 8
    h: int = 8
    speed: int = 1
    colkey: int | None = None
    costume_i: int = 0
    costumes: dict[str, tuple[int, int]] = field(default_factory=default_costumes)

    def draw(self):
        """
        Draw (render) character.
        """
        pyxel.blt(self.coord.x, self.coord.y, self.img, self.u, self.v, self.w, self.h, self.colkey)
    
    def set_costume(self, costume: tuple[int, int]):
        """
        Set costume based on spritemap coordinate.
        """
        self.u = costume[0]
        self.v = costume[1]

    def costume_toggle(self, costume_1: tuple[int, int], costume_2: tuple[int, int]):
        """
        Set costume based on current alternating costume index.
        """
        if self.costume_i:
            self.costume = costume_1
        else:
            self.costume = costume_2


# 3: Camera handling
@dataclass
class Camera:
    """
    A 2D camera that follows the player's movement.
    """
    speed: int = 1
    x: int = 0
    y: int = 0

    def __init__(self, player: Sprite):
       pyxel.camera()
       self.player = player
   
    def draw(self):
        #if not (self.player.coord.y_map < WINDOW_HEIGHT // 2 and self.y == self.player.speed):
        self.y = self.player.coord.y_map
        pyxel.bltm(0, 0, 0, self.x , self.y, 256, 256)


# 4: Text handling

# 5: Tick handling
class Ticker():
    """
    Retro games aren't meant to be smooth. However, Pyxel does support high frame rate. This timer can be used to limit a rate of something without messing with the game's actual FPS.
    """
    def __init__(self, limit: int):
        """
        Initialize a new tick timer.
        """
        self.limit = limit
        self.time_since_last_move = 0
        self.time_last_frame = 0
    
    def update(self):
        """
        Update tick counts.
        """
        time_this_frame = pyxel.frame_count
        self.dt = time_this_frame - self.time_last_frame
        self.time_last_frame = time_this_frame
        self.time_since_last_move += self.dt
    
    def get(self) -> bool:
        """
        Get status of tick.
        """
        if self.time_since_last_move >= self.limit:
            self.time_since_last_move = 0
            return True
        return False


# Functions
def map_to_view(self, camera_pos: Coordinate,) -> tuple[int, int] | bool:
    """
    Get position of object in screen based on its position on the map. Returns `False` if object is not within the camera boundary.
    """
    screen_x = self.x_map - camera_pos.x
    screen_y = self.y_map - camera_pos.y

    if screen_x < 0 or screen_x > WINDOW_WIDTH or screen_y < 0 or screen_y > WINDOW_HEIGHT:
        return False

    view_x = screen_x + (WINDOW_WIDTH // 2) - self.x
    view_y = screen_y + (WINDOW_HEIGHT // 2) - self.y

    return view_x, view_y
