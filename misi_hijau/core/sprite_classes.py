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

"""
Sprite base classes.
"""

# Imports
import pyxel

from dataclasses import dataclass
from abc import ABC, abstractmethod
from core import common
from typing import Optional

# XXX idea: sprite could automatically subscribe to events and we only need to specify an array of events.

# Classes for sprites

@dataclass
class SpriteCoordinate:
    # ↓ needs to be float because we use smooth movements and acceleration/drag might increment the coordinate values by some non-round number.
    x: float = 0 # x coord (viewport)
    y: float = 0 # y coord (viewport)
    x_map: float = 0 # x coord (relative to the map)
    y_map: float = 0 # y coord (relative to the map)

class Sprite(ABC):
    """
    A ("raw") sprite object class.
    """
    img: int = 0
    u: int = 0 # 2D coord of the spritesheet
    v: int = 0 # 2D coord of the spritesheet
    w: int = 8 # width
    h: int = 8 # height
    coord: SpriteCoordinate = SpriteCoordinate(-20, -20, -20, -20)
    colkey: Optional[int] = pyxel.COLOR_PURPLE
    keybindings: dict[str, common.KeyFunc] = {}
    statusbar_items: list[common.TextStatusbarItem | common.ProgressStatusbarItem] = []
    soundbank: dict[str, common.Sfx] = {}
    costumes: dict[str, tuple[int, int]] = {}

    def set_costume(self, costume: tuple[int, int]):
        """
        Set costume based on spritesheet coordinate.
        """
        self.u = costume[0]
        self.v = costume[1]

    def map_to_view(self, cam_y: float):
        """
        Get position of object in viewport based on its position on the map and assign it to the viewport x and y (`self.coord.x` and `self.coord.y`).
        Note: the x isn't required as argument because we only scroll in y direction.
        """

        self.coord.x = self.coord.x_map
        self.coord.y = self.coord.y_map - cam_y + common.WINDOW_HEIGHT / 2 
    
    def is_sprite_in_viewport(self) -> bool:
        """
        Returns `True` if sprite is within the camera boundary, else `False`.
        """
        
        # The self.h is added to calculate the actual border of the viewport where the
        # sprite will fully vanish
        # (if that makes sense)
        return not ((self.coord.x < -self.h) or (self.coord.x > common.WINDOW_WIDTH + self.h) or (self.coord.y < -self.h) or (self.coord.y > common.WINDOW_HEIGHT + self.h))

    def is_colliding(self, x: float, y: float, w: float, h: float) -> bool:
        """
        Returns `True` if sprite is colliding with another sprite with attributes specified by parameter `x`, `y`, `w`, and `h`.
        """
        return (
            self.coord.x + self.w > x
                and x + w > self.coord.x
                and self.coord.y + self.h > y
                and y + h > self.coord.y
        )
    
    def is_near(self, distance: float, x: float, y: float, w: int, h: int) -> bool:
        """
        Returns `True` if sprite is near other sprite with attributes specified by parameter `x`, `y`, `w`, and `h`.
        """
        return (
            self.coord.x + distance > x
                and x + w + distance > self.coord.x
                and self.coord.y + self.h + distance > y
                and y + h + distance > self.coord.y
        )

class SpriteHandler(ABC):
    """
    A handler for a sprite.
    """

    keybindings: dict[str, common.KeyFunc] = {}
    soundbank: dict[str, common.Sfx] = {}
    statusbar_items: list[common.TextStatusbarItem | common.ProgressStatusbarItem] = []

    @abstractmethod
    def draw(self):
        """
        Draw (render) sprite.
        """

    @abstractmethod
    def update(self):
        """
        Update sprite state.
        """
    
    @abstractmethod
    def init_level(self):
        """
        Function to be called on each new level.
        """
    
    @abstractmethod
    def restart_level(self):
        """
        Function to be called after restarting a level.
        """
    
class TilemapBasedSprite(ABC):
    """
    A tilemap-based sprite object class. These sprites are event-driven, meaning they don't need to implement the update and draw methods.
    """

    img: int = 0
    w: int = 8 # width
    h: int = 8 # height
    coord: SpriteCoordinate = SpriteCoordinate(-20, -20, -20, -20)
    colkey: Optional[int]
    keybindings: dict[str, common.KeyFunc] = {}
    soundbank: dict[str, common.Sfx] = {}
    costumes: dict[str, tuple[int, int]] = {}
    statusbar_items: list[common.TextStatusbarItem | common.ProgressStatusbarItem] = []

    @abstractmethod
    def init_level(self):
        """
        Function to be called on each new level.
        """
    
    @abstractmethod
    def restart_level(self):
        """
        Function to be called after restarting a level.
        """