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

"""
Level storing.
"""
from game.sprites.powerups import PowerUp
import pyxel
from core.common import (
    LevelMap,
    Level,
    MineralType,
    EnemyType,
    PowerUpType,
    PlayerShipType
)


# MAP 1
map_1_width = 32
map_1_height = 72
map_1_x = 0
map_1_y = 0
map_1 = LevelMap(map_1_x, map_1_y, map_1_width, map_1_height, [])

# MAP 2
map_2_width = 32
map_2_height = 104
map_2_x = 40
map_2_y = 0
map_2_powerups_map = [
    PowerUp(PowerUpType.HEALTH, 15, 77),
    PowerUp(PowerUpType.SPEED_BOOST, 16, 80)
]
map_2 = LevelMap(map_2_x, map_2_y, map_2_width, map_2_height, map_2_powerups_map)

# MAP 3
map_3_width = 32
map_3_height = 168
map_3_x = 80
map_3_y = 0
map_3 = LevelMap(map_3_x, map_3_y, map_3_width, map_3_height, [])

# Create list of levels
levels: list[Level] = [
    Level(1, map_1, PlayerShipType.SHIP1, EnemyType.ENEMY_1, MineralType.MINERAL_1, pyxel.COLOR_LIME, pyxel.COLOR_LIME, pyxel.COLOR_LIGHT_BLUE, 14, 3),
    Level(2, map_2, PlayerShipType.SHIP2, EnemyType.ENEMY_2, MineralType.MINERAL_2, pyxel.COLOR_CYAN, pyxel.COLOR_RED, pyxel.COLOR_PINK, 20, 4),
    Level(3, map_2, PlayerShipType.SHIP3, EnemyType.ENEMY_3, MineralType.MINERAL_3, pyxel.COLOR_GRAY, pyxel.COLOR_PINK, pyxel.COLOR_YELLOW, 35, 5) # ship doesn't have flame
]

LEVELS_COUNT = len(levels)