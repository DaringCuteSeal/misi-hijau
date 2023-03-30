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
from ..common import (
    WINDOW_WIDTH,
    ALPHA_COL
)
from ..utils import tile_to_real
from ..game_handler import GameComponents
from .. import events
from . import UIComponent, UIComponentCoordinate

class HealthBar(UIComponent):
    w = 8
    h = 8
    costume = (48, 48)
    def_gap_x = 1
    edge_gap = 4
    coord = UIComponentCoordinate(0, 0)

    def __init__(self, game: GameComponents, health_count: int):
        self.game = game
        self.game.event_handler.add_handler(events.PlayerHealthChange.name, self.change_health_count)
        self.health_count = health_count
        self._recalculate()
    
    def _draw(self):
        if self.health_count > 0:
            x_prev = self.coord.x
            for i in range(0, self.health_count): # type: ignore
                x = x_prev + self.w + self.def_gap_x
                pyxel.blt(x, self.coord.y, 0, self.costume[0], self.costume[1], self.w, self.h, ALPHA_COL)
                x_prev = x

    def change_health_count(self, value: int):
        self.health_count += value
        self._recalculate

    def _recalculate(self):
        self.coord.x = WINDOW_WIDTH - pyxel.TILE_SIZE - self.health_count * self.def_gap_x - tile_to_real(self.health_count) - self.edge_gap
        self.coord.y = self.def_gap_x + self.edge_gap