# Copyright 2023 Cikitta Tjok <daringcuteseal@gmail.com>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pyxel
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional

# Common classes and functions for many files including utilities

# Constants
ALPHA_COL = pyxel.COLOR_PURPLE
WINDOW_WIDTH = 256
WINDOW_HEIGHT = 256
TILE_SIZE = 8

# Classes
class Direction(Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3

class SoundType(Enum):
    AUDIO = 0
    MUSIC = 1

class PlayerShip(Enum):
    SHIP1 = 0
    SHIP2 = 1
    SHIP3 = 2

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
    hold_time: Optional[int] = None
    repeat_time: Optional[int] = None

@dataclass
class Sfx():
    """
    An SFX entry.
    """
    soundtype: SoundType
    channel: int
    index: int = 0
    loop: bool = False

@dataclass
class LevelMap:
    """
    A level map. All values are in tilemap scale (TILE_SIZE)
    """
    map_x: int # Offset x of tilemap
    map_y: int # Offset y of tilemap
    level_width: int
    level_height: int
    enemies_map: list[tuple[int, int]]

@dataclass
class Level:
    """
    A level.
    """
    idx: int
    levelmap: LevelMap
    ship: PlayerShip
    max_minerals: int
    bullet_color: int

@dataclass
class StatusbarItem:
    """
    Item to be displayed in the statusbar.
    """
    function: Callable[[], str] # unction that returns a string.
    color: int

# Functions
def tile_to_real(size: int) -> int:
    """
    Get real tile size from a tilemap scale.
    """
    return size * TILE_SIZE

def round_to_tile(size: int) -> int:
    return pyxel.ceil(size / TILE_SIZE) * TILE_SIZE