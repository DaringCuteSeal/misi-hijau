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

from game.config import *

"""
Common classes and functions for many files including utilities.
"""

# Constants
ALPHA_COL = pyxel.COLOR_PURPLE
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
    ENEMY_1 = 0 # Grug / MulticoloredSplotch
    ENEMY_2 = 1 # Phong / ObeseSpider
    ENEMY_3 = 2 # Squidge / PinkRetardWithLegs

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
    Class with key and its associated function.
    """
    binding: list[int]
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

@dataclass
class Level:
    """
    A level.
    """
    idx: int
    levelmap: LevelMap
    ship_type: PlayerShipType
    enemy_type: EnemyType
    mineral_type: MineralType
    bullet_color: int
    enemies_statusbar_color: int
    minerals_statusbar_color: int
    minerals_count: int
    max_health: int

    minerals_all_collected = False
    enemies_all_eliminated = False

@dataclass
class Icon:
    """
    Basic image from the spritesheet.
    """
    img: int
    u: int 
    v: int 
    w: int
    h: int
    colkey: Optional[int] = pyxel.COLOR_PURPLE

@dataclass
class TextStatusbarItem:
    """
    String to be displayed at the statusbar.
    """
    idx: int
    function: Callable[[], str]
    color: int
    gap: int = 2
    custom_coords: bool = False
    x: int = 0
    y: int = 0

    def __post_init__(self):
        self.string: str = ""

    def update(self):
        self.string = self.function()

    def draw(self):
        pyxel.text(self.x, self.y, self.string, self.color)

@dataclass
class ProgressStatusbarItem:
    """
    A progress bar to be displayed at the statusbar.
    """
    idx: int
    max_val: int
    function: Callable[[], int]
    border_col: int
    progress_col: int
    bar_width: int
    bar_height: int
    icon: Optional[Icon] = None
    text_over_bar: Optional[str] = None
    text_over_bar_col: int = pyxel.COLOR_WHITE
    gap: int = 2
    icon_gap: int = 2 # gap from icon to bar
    custom_coords: bool = False
    x: int = 0
    y: int = 0

    def __post_init__(self):
        self._recalculate()
        self.height = 0
        self.text_x = self.x
        self.text_y = self.y

    def new_max_val(self, max_val: int):
        """
        Set a new max value.
        """
        self.max_val = max_val
        self._recalculate()

    def _recalculate(self):
        try:
            self.pixels_per_val = (self.bar_width - 2) / self.max_val # set pixels per val
        except ZeroDivisionError: # if the max_amount is 0:
            self.pixels_per_val = self.bar_width # set pixels_per_val to the width instead

        self._recalculate_bar_coords()
        
    def post_recalculate(self):
        self._recalculate_bar_coords()
        self._recalculate_text_coords()

    def _recalculate_text_coords(self):
        if self.text_over_bar:
            self.text_x = self.bar_x + (self.bar_width - len(self.text_over_bar * pyxel.FONT_WIDTH)) // 2
            self.text_y = self.bar_y + (self.bar_height - pyxel.FONT_HEIGHT) // 2

    def _recalculate_bar_coords(self):
        if self.icon:
            self.height = max(self.icon.h, self.bar_height)
            self.bar_y = self.y + (self.icon.h - self.bar_height) // 2
            self.bar_x = self.x + self.icon.w + self.icon_gap
        else:
            self.height = self.bar_height
            self.bar_y = self.y
            self.bar_x = self.x

    def _draw_text_over_bar(self):
        if self.text_over_bar:
            pyxel.text(self.text_x, self.text_y, self.text_over_bar, self.text_over_bar_col)

    def _draw_icon_if_icon(self):
        if self.icon:
            pyxel.blt(self.x, self.y, self.icon.img, self.icon.u, self.icon.v, self.icon.w, self.icon.h, self.icon.colkey)

    def update(self):
        self.value = self.function()

    def draw(self):
        pyxel.rectb(self.bar_x, self.bar_y, self.bar_width, self.bar_height, self.border_col) # border
        pyxel.rect(self.bar_x + 1, self.bar_y + 1, self.value * self.pixels_per_val, self.bar_height - 2, self.progress_col) # progress
        self._draw_icon_if_icon()
        self._draw_text_over_bar()
    
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