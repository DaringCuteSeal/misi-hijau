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

import pyxel

from game.common import (
    Level,
    LevelMap,
    PlayerShipType,
    MineralType
)


# MAP 1
map_1_width = 32
map_1_height = 72
map_1_x = 0
map_1_y = 0
enemies_map_1: list[tuple[int, int]] = [
    (1, 50), (3, 50), (5, 50), (7, 50), (9, 50), (11, 50),
    (13, 50), (15, 50), (17, 50), (19, 50), (21, 50),
    (23, 50), (25, 50), (27, 50), (29, 50),

    (2, 11), (3, 11), (4, 10), (5, 9), (6, 8), (7, 8),
    (8, 8), (9, 8), (10, 8), (11, 8), (12, 8),
    (13, 9), (14, 10), (15, 11),

    (16, 11), (17, 10), (18, 9), (19, 8), (20, 8),
    (21, 8), (22, 8), (23, 8), (24, 8), (25, 8),
    (26, 9), (27, 10), (28, 11), (29, 11)
]

map_1 = LevelMap(map_1_x, map_1_y, map_1_width, map_1_height, enemies_map_1, [])

# MAP 2
map_2_width = 32
map_2_height = 104
map_2_x = 40
map_2_y = 0
enemies_map_2: list[tuple[int, int]] = [
    
]

map_2 = LevelMap(map_2_x, map_2_y, map_2_width, map_2_height, enemies_map_2, [])

# MAP 3
map_3 = LevelMap(0, 0, 32, 72, enemies_map_2, [])

# Create list of levels
levels: list[Level] = [
    Level(1, map_1, PlayerShipType.SHIP1, MineralType.MINERAL_1, pyxel.COLOR_LIME, 14, 3),
    Level(2, map_2, PlayerShipType.SHIP2, MineralType.MINERAL_2, pyxel.COLOR_CYAN, 20, 4),
    Level(3, map_2, PlayerShipType.SHIP3, MineralType.MINERAL_3, pyxel.COLOR_GRAY, 35, 5) # ship doesn't have flame
]