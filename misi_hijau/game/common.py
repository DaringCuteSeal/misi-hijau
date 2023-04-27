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
from typing import Any, Callable, Optional
from time import time

"""
Common classes and functions for many files including utilities.
"""

# Constants
ALPHA_COL = pyxel.COLOR_PURPLE
WINDOW_WIDTH = 256
WINDOW_HEIGHT = 256
BLANK_UV = (0, 0)
MAP_Y_OFFSET_TILES = WINDOW_HEIGHT // 2 // pyxel.TILE_SIZE # the map y coordinate is offset by half the screen size because of how the player movement is handled.

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

class EnemyType(Enum):
    ENEMY_1 = 0 # Krelth/Grug
    ENEMY_2 = 1 # Naxor/Phong
    ENEMY_3 = 2 # Octyca/Squidge

class PowerUpType(Enum):
    HEALTH = 0
    SHIELD = 1
    SPEED_BOOST = 2

class KeyTypes(Enum):
    BTN = 0
    BTNP = 1

@dataclass
class KeyFunc:
    """
    An object with a key and its associated function.
    """
    binding: int
    func: Callable[[], Any]
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

@dataclass
class PowerUp:
    powerup_type: PowerUpType
    x: int
    y: int
    w = 8
    h = 8

@dataclass
class LevelMap:
    """
    A level map. All values are in tilemap scale (pyxel.TILE_SIZE)
    """
    map_x: int # Offset x of tilemap
    map_y: int # Offset y of tilemap
    level_width: int
    level_height: int
    powerups_map: list[PowerUp]

class Level:
    """
    A level.
    """
    def __init__(self, idx: int, levelmap: LevelMap, ship_type: PlayerShipType, enemy_type: EnemyType, mineral_type: MineralType, bullet_color: int, max_minerals: int, max_health: int):
        self.idx = idx
        self.levelmap = levelmap
        self.ship_type = ship_type
        self.enemy_type = enemy_type
        self.mineral_type = mineral_type
        self.bullet_color = bullet_color
        self.max_minerals = max_minerals
        self.max_health = max_health

        self.minerals_all_collected = False
        self.enemies_all_eliminated = False

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

class TimerItem:
    """
    A Timer item.
    """
    def __init__(self, time_limit: float, timer_id: str = "timer_item"):
        self.timer_id = timer_id
        self.time_limit = time_limit
        self.start_timestamp = time()
        self._function_when_over: Optional[Callable[[], None]] = None

    def when_over(self, function: Callable[[], None]):
        """
        Set the function to run when the timer is over.
        """
        self._function_when_over = function

    def is_over(self) -> bool:
        """
        Check whether the timer is over.
        """
        time_now = time()
        return time_now - self.start_timestamp > self.time_limit

    def run_function(self):
        """
        Run function that's set to run after timer is over.
        """
        self._function_when_over() if self._function_when_over else None