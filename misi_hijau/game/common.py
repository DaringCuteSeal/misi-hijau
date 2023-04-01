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

"""
Common classes and functions for many files including utilities.
"""

# Constants
ALPHA_COL = pyxel.COLOR_PURPLE
WINDOW_WIDTH = 256
WINDOW_HEIGHT = 256

# Classes
class Direction(Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3

class SoundType(Enum):
    AUDIO = 0
    MUSIC = 1

class PlayerShipType(Enum):
    SHIP1 = 0
    SHIP2 = 1
    SHIP3 = 2

class MineralType(Enum):
    MINERAL_1 = 0
    MINERAL_2 = 1
    MINERAL_3 = 2

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
    idx: int = 0
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
    powerups_map: list[tuple[int, int]] | None

class Level:
    """
    A level.
    """
    def __init__(self, idx: int, levelmap: LevelMap, ship_type: PlayerShipType, mineral_type: MineralType, bullet_color: int, max_minerals: int, max_health: int):
        self.idx = idx
        self.levelmap = levelmap
        self.ship_type = ship_type
        self.mineral_type = mineral_type
        self.bullet_color = bullet_color
        self.max_minerals = max_minerals
        self.max_health = max_health
        self.enemies_count = len(self.levelmap.enemies_map)

@dataclass
class StatusbarItem:
    """
    Item to be displayed in the statusbar.
    """
    idx: int
    function: Callable[[], str] # function that returns a string
    color: int
    update_interval: float = 1
    custom_coords: bool = False
    x: int = 0
    y: int = 0