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
MAP_HEIGHT = 128 * 8

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
    Create a new key listener object.
    """
    binding: int
    func: Callable[[], None]
    btn_type: KeyTypes = KeyTypes.BTN
    active: bool = True

class KeyListener:
    # TODO: group keybindings by game object so same label can be used

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
    x: int = 0
    y: int = 0
    x_map: int = 0
    y_map: int = 0

def default_costumes():
    return {}

@dataclass
class Sprite:
    coord: Coordinate
    img: int = 0
    u: int = 0
    v: int = 0
    w: int = 8
    h: int = 8
    colkey: int | None = None
    costumes: dict[str, tuple[int, int]] = field(default_factory=default_costumes)

    def draw(self):
        pyxel.blt(self.coord.x, self.coord.y, self.img, self.u, self.v, self.w, self.h, self.colkey)


# 3: Camera handling
@dataclass
class Camera:
    speed: int = 1
    x: int = 0
    y: int = 0

    def __init__(self, player: Sprite):
       pyxel.camera()
       self.player = player
   
    def draw(self):
        self.y = self.player.coord.y_map
        pyxel.bltm(0, 0, 0, self.x , self.y, 256, 256)


# 4: Text handling

# 5: Tick handling
class Ticker():
    def __init__(self):
        self.time_since_last_move = 0
        self.time_last_frame = 0
    
    def update(self):
        self.time_this_frame = pyxel.frame_count
        self.dt = self.time_this_frame - self.time_last_frame
        self.time_last_frame = self.time_this_frame
        self.time_since_last_move += self.dt
    

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