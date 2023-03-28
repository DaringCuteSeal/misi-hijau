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

from . import Sprite
from ..game_handler import GameStateManager
from .. import events
from ..common import MineralType, Sfx, SoundType, StatusbarItem
from ..utils import real_to_tile
import pyxel

class MineralHandler(Sprite):
    costumes = {
        "mineral_1": (1, 2),
        "mineral_2": (1, 3),
        "mineral_3": (0, 3)
    }

    soundbank = {
        "mineral_increment": Sfx(SoundType.AUDIO, 3, 12)
    }

    def __init__(self, game: GameStateManager):
        self.game = game
        self.game.event_handler.add_handler(events.MineralsCheck.name, self.player_collision_check_handler)
        self.game.statusbar.add(StatusbarItem(self.get_minerals_count, pyxel.COLOR_WHITE))

        self.level = self.game.level_handler.get_curr()
        mineral_type = self.level.mineral_type
        match mineral_type:
            case MineralType.MINERAL_1:
                self.mineral_costume = self.costumes["mineral_1"]
            case MineralType.MINERAL_2:
                self.mineral_costume = self.costumes["mineral_2"]
            case MineralType.MINERAL_3:
                self.mineral_costume = self.costumes["mineral_3"]
    
    def draw(self):
        pass

    def update(self):
        pass

    def player_collision_check_handler(self, player_x_map: float, player_y_map: float, player_h: int) -> bool:
        # +1 tile here to count the centered player coordinate.
        x = real_to_tile(player_x_map) + 1
        y = real_to_tile(player_y_map) + 17 # the coordinate system is offset by 16 tiles because of the player's system
        tilemap = pyxel.tilemap(0).pget(x, y)
        if tilemap == (self.mineral_costume):
            self.game.soundplayer.play(self.soundbank["mineral_increment"])
            self.level.progress.increment_minerals(1)
            pyxel.tilemap(0).pset(x, y, (0, 0))
            return True
        return False
    
    def get_minerals_count(self) -> str:
        return f"Minerals collected: {self.level.progress.minerals:>2} / {self.level.max_minerals}"