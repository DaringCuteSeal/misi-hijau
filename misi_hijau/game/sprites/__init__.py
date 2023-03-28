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

# Imports
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from .. import common

# Classes for sprites

@dataclass
class SpriteCoordinate:
    # ↓ needs to be float because we use smooth movements and acceleration/drag might increment the coordinate values by some non-round number.
    x: float = 0
    y: float = 0
    x_map: float = 0
    y_map: float = 0

class SpriteHandler(ABC):
    pass

class Sprite(ABC):
    """
    A sprite object class with some predefined functions to make costume handling easier.
    """
    coord: SpriteCoordinate
    img: int = 0
    u: int = 0
    v: int = 0
    w: int = 8
    h: int = 8
    speed: float = 1
    colkey: int | None = None
    costume_i: int = 0
    keybindings: dict[str, common.KeyFunc] = field(default_factory=dict[str, common.KeyFunc])
    soundbank: dict[str, common.Sfx] = field(default_factory=dict[str, common.Sfx])
    costumes: dict[str, tuple[int, int]] = field(default_factory=dict[str, tuple[int, int]])

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

    def reset(self):
        """
        Function to be run when level restarts.
        """

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

    def map_to_view(self, cam_y: float):
        """
        Get position of object in viewport based on its position on the map and assign it to the viewport x and y (`self.coord.x` and `self.coord.y`). Returns True if sprite is within camera boundary; else returns False.
        Note: the x isn't required as argument because we only scroll in y direction.
        """

        self.coord.x = self.coord.x_map
        self.coord.y = self.coord.y_map - cam_y + common.WINDOW_HEIGHT / 2 
    
    def is_sprite_in_viewport(self) -> bool:

        if self.coord.x < -10 or self.coord.x > common.WINDOW_WIDTH or self.coord.y < -10 or self.coord.y > common.WINDOW_HEIGHT:
            return False
        else:
            return True

    def is_colliding(self, x: float, y: float, w: float, h: float) -> bool:
        if (
            self.coord.x + self.w > x
            and x + w > self.coord.x
            and self.coord.y + self.h > y
            and y + h > self.coord.y
        ):
            return True
        return False