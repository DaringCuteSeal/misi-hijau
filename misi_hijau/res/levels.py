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

from game.base import (
    Level,
    LevelMap,
    PlayerShip
)

enemies_map: list[tuple[int, int]] = [
    (1, 53), (3, 53), (5, 53), (7, 53), (9, 53), (11, 53),
    (13, 53), (15, 53), (17, 53), (19, 53), (21, 53),
    (23, 53), (25, 53), (27, 53), (29, 53)
]
map_1 = LevelMap(0, 0, 32, 72, enemies_map)
map_2 = LevelMap(40, 0, 32, 104, enemies_map)
map_3 = LevelMap(0, 0, 32, 72, enemies_map)

levels: list[Level] = [
    Level(1, map_1, PlayerShip.SHIP1, 15, pyxel.COLOR_LIME),
    Level(2, map_2, PlayerShip.SHIP2, 15, pyxel.COLOR_CYAN),
    Level(3, map_3, PlayerShip.SHIP3, 15, pyxel.COLOR_GRAY) # note: ship does not have extra flame
]