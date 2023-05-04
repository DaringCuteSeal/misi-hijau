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
from core.common import (
    WINDOW_WIDTH,
    ALPHA_COL
)
from core.utils import tile_to_real
from core.game_handler import GameHandler
from core.game_ui_classes import UIComponent, UIComponentCoordinate
from .. import events

class HealthBar(UIComponent):
    """
    A game healthbar.
    """
    w = 8
    h = 8
    costume = (48, 48)
    def_gap_x = 1
    edge_gap = 4
    coord = UIComponentCoordinate(0, 0)

    def __init__(self, game_handler: GameHandler):
        self.game_handler = game_handler
        self.active = False # UI components are instantiated during the very start of the game (since the intro; not the main game) so we deactivate it when this healthbar is instantiated.
        self.game_handler.game_components.event_handler.add_handler(events.StartGame.name, lambda: self._alter_healthbar_visibility(True)) # show the healthbar on game start
        self.game_handler.game_components.event_handler.add_handler(events.StopGameLoop.name, lambda: self._alter_healthbar_visibility(False)) # hide healthbar when game loop is stopped
        self.game_handler.game_components.event_handler.add_handler(events.PlayerHealthChange.name, self.change_health_count)
        self.setup()
    
    def setup(self):
        self.health_count = self.game_handler.levelhandler.get_curr_lvl().max_health
        self._recalculate()

    def _draw(self):
        if self.health_count > 0:
            x_prev = self.coord.x
            for _ in range(0, self.health_count):
                x = x_prev + self.w + self.def_gap_x
                pyxel.blt(x, self.coord.y, 0, self.costume[0], self.costume[1], self.w, self.h, ALPHA_COL)
                x_prev = x

    def change_health_count(self, change_value: int):
        self.health_count += change_value
        self._recalculate

    def _recalculate(self):
        self.coord.x = WINDOW_WIDTH - pyxel.TILE_SIZE - self.health_count * self.def_gap_x - tile_to_real(self.health_count) - self.edge_gap
        self.coord.y = self.def_gap_x + self.edge_gap

    def _alter_healthbar_visibility(self, state: bool):
        self.active = state

    def init_level(self):
        self._alter_healthbar_visibility(True)
        self.setup()
    
    def restart_level(self):
        self._alter_healthbar_visibility(True)
        self.setup()