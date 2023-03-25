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
from .. import base

# Classes for sprites

@dataclass
class SpriteCoordinate:
    # ↓ needs to be float because we use smooth movements and acceleration/drag might increment the coordinate values by some non-round number.
    x: float = 0
    y: float = 0
    x_map: float = 0
    y_map: float = 0

@dataclass
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
    # XXX: maybe these fields can be avoided if we just declare em in __init__()?
    keybindings: dict[str, base.KeyFunc] = field(default_factory=dict[str, base.KeyFunc])
    soundbank: dict[str, base.Sfx] = field(default_factory=dict[str, base.Sfx])
    costumes: dict[str, tuple[int, int]] = field(default_factory=dict[str, tuple[int, int]])

    @abstractmethod
    def draw(self):
        """
        Draw (render) sprite.
        """
        pass
    
    @abstractmethod
    def update(self):
        pass
    
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
        self.coord.y = self.coord.y_map - cam_y + base.WINDOW_HEIGHT / 2 
    
    def is_sprite_in_viewport(self) -> bool:

        if self.coord.x < -10 or self.coord.x > base.WINDOW_WIDTH or self.coord.y < -10 or self.coord.y > base.WINDOW_HEIGHT:
            return False
        else:
            return True

class SpriteGroup:
    def __init__(self, sprites: dict[str, Sprite], game: base.GameStateManager):
        self.sprites = sprites
        self.game = game
    
    def update(self):
        for i in self.sprites:
            self.sprites[i].update()

    def render(self):
        for i in self.sprites:
            self.sprites[i].draw()

        self.game.statusbar.draw()