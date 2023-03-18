# Copyright 2023 Cikitta Tjok

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

### Utilities for a better workflow

# Imports
import pyxel
from typing import Callable
from enum import Enum
from dataclasses import dataclass

# Enums
class Direction(Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3

class SoundType(Enum):
    AUDIO = 0
    MUSIC = 1

# Other Constants
ALPHA_COL = pyxel.COLOR_PURPLE
WINDOW_WIDTH = 256
WINDOW_HEIGHT = 256
MAP_WIDTH = 24 * 8
MAP_HEIGHT = 97 * 8
TILE_SIZE = 8

# Functions for Classes
# XXX remove if not needed
def tile_to_real(size: int):
    """
    Get real tile size from a tilemap scale.
    """
    return size * TILE_SIZE


# 1: Keyboard handling
class KeyTypes(Enum):
    BTN = 0
    BTNP = 1
    BTNP_REPEAT = 2

@dataclass
class KeyFunc:
    """
    An object with a key and its associated function.
    """
    binding: int
    func: Callable[[], None]
    btn_type: KeyTypes = KeyTypes.BTN
    active: bool = True
    hold_time: int | None = None
    repeat_time: int | None = None

class KeyListener:
    """
    A Key listener that is able to execute functions.
    """
    # TODO: group keybindings by game object so same keybindings with same name can exist.

    def __init__(self):
        self.checks: dict[str, KeyFunc] = {}
    
    def append(self, keyfunc: dict[str, KeyFunc],):
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
                        if pyxel.btnp(check[k].binding, hold=check[k].hold_time, repeat=check[k].repeat_time):
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

# 3: Camera handling
@dataclass
class Camera:
    """
    A 2D camera.
    """
    speed: int = 1
    x: int = 0
    y: int = 0

    def __init__(self):
       pyxel.camera()
   
    def draw(self):
        pyxel.bltm(0, 0, 0, self.x , self.y, 256, 256)


# 4: Text handling

# 5: Tick handling
class Ticker():
    """
    Retro games aren't meant to be smooth. However, Pyxel supports high frame rate. This timer can be used to limit a rate of something without messing with the game's actual FPS.
    """
    def __init__(self):
        """
        Initialize a new tick timer.
        """
        self.time_since_last_move = 0
        self.time_last_frame = 0
    
    def update(self):
        """
        Update tick counts. Should be run on every game tick by the main game process. Shouldn't be called within sprites.
        """
        time_this_frame = pyxel.frame_count
        self.dt = time_this_frame - self.time_last_frame
        self.time_last_frame = time_this_frame
        self.time_since_last_move += self.dt
    
    def get(self, limit: int) -> bool:
        """
        Get status of tick.
        """
        if self.time_since_last_move >= limit:
            self.time_since_last_move = 0
            return True
        return False


# 6. Sound handling
class Sfx():
    soundtype: SoundType
    channel: int
    index: int = 0
    loop: bool = False

@dataclass
class Sound():
    sounds: dict[str, Sfx]
    ch: int = 0

    def play(self, name: str):
        match(self.sounds[name].soundtype):
            case SoundType.AUDIO:
                pyxel.play(self.ch, self.sounds[name].index, loop=self.sounds[name].loop)
            case SoundType.MUSIC:
                pyxel.playm(self.sounds[name].index, loop=self.sounds[name].loop)


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
