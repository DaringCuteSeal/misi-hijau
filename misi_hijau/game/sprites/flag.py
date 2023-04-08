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

from . import TilemapBasedSprite
from game.game_handler import GameComponents
from game.common import Level
import game.events as events

FLAG_UV = (2, 7)

class LevelFlag(TilemapBasedSprite):
    def __init__(self, level: Level, game: GameComponents):
       self.level = level
       self.game = game 
       self.game.event_handler.add_handler(events.TilemapPlayerCheck.name, self.player_level_completed_check)
    
    def _is_level_complete(self) -> bool:
        return self.level.minerals_all_collected and self.level.enemies_all_eliminated

    def player_level_completed_check(self, uv: tuple[int, int], tile_x: int, tile_y: int):
        if self._is_level_complete():
            if uv == FLAG_UV:
                self.game.event_handler.trigger_event(events.LevelNext)
