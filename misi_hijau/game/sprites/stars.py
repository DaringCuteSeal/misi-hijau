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

from dataclasses import dataclass
import pyxel
from ..base import (
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    GameStateManager,
    SpriteObj,
)

@dataclass
class Stars(SpriteObj):
    """
    Stars that scrolls in the background.
    """
    # I won't make a Star class cuz that could be computationally expensive.
    # The tuple is structured is like (x, y, speed)
    def __init__(self, num_stars: int, game: GameStateManager):
        self.camera = game.camera
        self.stars: list[tuple[float, float, float]] = []
        for i in range(0, num_stars): # type: ignore
            self.stars.append((
                pyxel.rndi(0, WINDOW_WIDTH),
                pyxel.rndi(0, WINDOW_HEIGHT),
                pyxel.rndf(0.1, 0.3)
            ))
        
    def update(self):
        for i, (x, y, speed) in enumerate(self.stars):
            y += self.camera.dir_y / (13 + speed*2)
            if y >= WINDOW_HEIGHT:
                y -= WINDOW_HEIGHT
            self.stars[i] = (x, y, speed)

    def draw(self):
        for x, y, speed in self.stars:
            pyxel.pset(x, y, pyxel.COLOR_CYAN if speed > 0.2 else pyxel.COLOR_NAVY)
