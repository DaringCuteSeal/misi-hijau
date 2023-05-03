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

from core.sprite_classes import TilemapBasedSprite
from core.game_handler import GameHandler
from game import events

class LevelFlag(TilemapBasedSprite):
    FLAG_UV = (2, 7)

    def __init__(self, game_handler: GameHandler):
       self.game_handler = game_handler
       self.game_handler.game_components.event_handler.add_handler(events.TilemapPlayerCheck.name, self.player_level_completed_check)
       self.setup()
    
    def setup(self):
        self.level = self.game_handler.levelhandler.get_curr_lvl()
        self.level.minerals_all_collected = False
        self.level.enemies_all_eliminated = False

    def _is_level_complete(self) -> bool:
        return self.level.minerals_all_collected and self.level.enemies_all_eliminated

    def init_level(self):
        self.setup()

    def restart_level(self):
        self.setup()

    def player_level_completed_check(self, uv: tuple[int, int], tile_x: int, tile_y: int): # FIXME: Some functions still call this function with these arguments. If one removes them, breakage will occur. Refactoring should be done later
        if self._is_level_complete() and uv == self.FLAG_UV:
            self.game_handler.game_components.event_handler.trigger_event(events.LevelNext)
