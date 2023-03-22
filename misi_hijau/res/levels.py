# Copyright 2023 Cikitta Tjok

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from game.base import (
    Level,
    LevelMap,
    PlayerShip
)

map_1 = LevelMap(0, 0, 32, 72)
map_2 = LevelMap(0, 0, 32, 72)
map_3 = LevelMap(0, 0, 32, 72)

levels: list[Level] = [
    Level(1, PlayerShip.SHIP1, map_1),
    Level(2, PlayerShip.SHIP2, map_2),
    Level(3, PlayerShip.SHIP3, map_3) # note: ship does not have extra flame
]