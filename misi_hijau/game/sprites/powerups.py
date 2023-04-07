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
import pyxel
from game.sprites import Sprite
from game.common import PowerUpType, PowerUp, Level
from game.game_handler import GameComponents
from game.utils import tile_to_real

class PowerUpHandler(Sprite):
    costumes: dict[str, tuple[int, int]] = {
            "health": (16, 48),
            "shield": (24, 48),
            "speed_boost": (24, 56)
        }

    def __init__(self, level: Level, game: GameComponents):
        self.game = game
        self.levelmap = level.levelmap
        self.powerup_coordinates_list = self.levelmap.powerups_map
    
    def append_powerup_list(self, powerup_coordinates_list: list[PowerUp]):
        self.powerup_coordinates_list.extend(powerup_coordinates_list)
    
    def get_powerup_uv_from_type(self, powerup_type: PowerUpType) -> tuple[int, int]:
        match powerup_type:
            case PowerUpType.HEALTH:
                return self.costumes["health"]
            case PowerUpType.SHIELD:
                return self.costumes["shield"]
            case PowerUpType.SPEED_BOOST:
                return self.costumes["speed_boost"]

    def spawn(self):
        tilemap = pyxel.tilemap(0)
        for powerup in self.powerup_coordinates_list:
            x = powerup.x + tile_to_real(self.levelmap.level_width)
            y = powerup.y + tile_to_real(self.levelmap.level_height)
            tilemap.pset(x, y, self.get_powerup_uv_from_type(powerup.powerup_type))
    
    def update(self):
        pass

    def draw(self):
        pass