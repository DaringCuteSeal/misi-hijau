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

from dataclasses import dataclass
import pyxel
from core.common import (
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from core.game_handler import GameHandler
from .. import events

@dataclass
class Stars: # kinda a UI component but is drawn before everything else so the component rules don't apply to this class
    """
    Stars that scrolls in the background.
    """
    def __init__(self, num_stars: int, game_handler: GameHandler):
        self.num_stars = num_stars
        game_handler.game_components.event_handler.add_handler(events.StarsScroll.name, self.update)
        self.camera = game_handler.game_components.camera
        self.stars_list = self.generate_stars_list(self.num_stars)

    def generate_stars_list(self, num_stars: int) -> list[tuple[float, float, float]]:
        stars_list: list[tuple[float, float, float]] = []
        for _ in range(0, num_stars): # type: ignore
            stars_list.append((
                pyxel.rndi(0, WINDOW_WIDTH),
                pyxel.rndi(0, WINDOW_HEIGHT),
                pyxel.rndf(1, 5)
            ))
        
        return stars_list
        
    def update(self):
        for i, (x, y, speed) in enumerate(self.stars_list):
            y += (self.camera.dir_y / (8 + speed)) * -1
            if y >= WINDOW_HEIGHT:
                y -= WINDOW_HEIGHT
            if y <= 0:
                y = WINDOW_HEIGHT
            self.stars_list[i] = (x, y, speed)

    def draw(self):
        for x, y, speed in self.stars_list:
            pyxel.pset(x, y, pyxel.COLOR_CYAN if speed < 3 else pyxel.COLOR_NAVY)
    
    def init_level(self):
        self.stars_list = self.generate_stars_list(self.num_stars)

    def restart_level(self):
        pass