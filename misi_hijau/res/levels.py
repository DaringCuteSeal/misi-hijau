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

enemies_map_1: list[tuple[int, int]] = [
    (1, 50), (3, 50), (5, 50), (7, 50), (9, 50), (11, 50),
    (13, 50), (15, 50), (17, 50), (19, 50), (21, 50),
    (23, 50), (25, 50), (27, 50), (29, 50)
]
map_1 = LevelMap(0, 0, 32, 72, enemies_map_1, powerups_map=None)

enemies_map_2: list[tuple[int, int]] = [
    
]
map_2 = LevelMap(40, 0, 32, 104, enemies_map_2, None)
map_3 = LevelMap(0, 0, 32, 72, enemies_map_2, None)

levels: list[Level] = [
    Level(1, map_1, PlayerShipType.SHIP1, MineralType.MINERAL_1, pyxel.COLOR_LIME, 14, 3),
    Level(2, map_2, PlayerShipType.SHIP2, MineralType.MINERAL_2, pyxel.COLOR_CYAN, 15, 4),
    Level(3, map_2, PlayerShipType.SHIP3, MineralType.MINERAL_3, pyxel.COLOR_GRAY, 15, 5) # ship doesn't have flame
]