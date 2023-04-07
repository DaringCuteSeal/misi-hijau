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
Common utilities.
"""
import pyxel

# Tick handling
class Ticker:
    """
    Retro games aren't meant to be smooth. However, Pyxel supports high frame rate. This timer can be used to limit a rate of something without messing with the game's actual FPS.
    """
    def __init__(self, frame_limit: float):
        """
        Initialize a new tick timer for an entity.
        """
        self.time_since_last_move = 0
        self.time_last_frame = 0
        self.limit = frame_limit
    
    def update(self):
        """
        Update tick counts. Should be run on every game tick by sprite.
        """
        time_this_frame = pyxel.frame_count
        self.dt = time_this_frame - self.time_last_frame
        self.time_last_frame = time_this_frame
        self.time_since_last_move += self.dt
    
    def get(self) -> bool:
        """
        Get status of tick.
        """
        
        if self.time_since_last_move * 10 >= self.limit * 10:
            self.time_since_last_move = 0
            return True
        return False

# Functions
def tile_to_real(size: int) -> int:
    """
    Get real size in pixel from a tilemap size.
    """
    return size * pyxel.TILE_SIZE

def real_to_tile(size: float) -> int:
    """
    Get tilemap size from real pixel size.
    """
    size = size // pyxel.TILE_SIZE
    return pyxel.floor(size)

def round_to_tile(size: float) -> int:
    """
    Round a number to closest multiple of TILE_SIZE.
    """
    return pyxel.ceil(size / pyxel.TILE_SIZE) * pyxel.TILE_SIZE

def generate_random_map_matrix(num_tiles: int, map_w: int, map_h: int, map_x: int, map_y: int) -> list[tuple[int, int]]:
    """
    Generate a random map matrix: an array containing tuples of coordinates. `w` and `h` is in tilemap scale.
    """
    map_matrix: list[tuple[int, int]] = []
    while len(map_matrix) < num_tiles:
        # The extra 1 offset is needed so the player can *actually* collect the item. Also is just a nice padding.
        x = pyxel.rndi(pyxel.TILE_SIZE + 1, map_w - 1) + map_x
        y = pyxel.rndi(16 + 1, map_h - 1) + map_y # the map is offset by 16 tiles
        if (x, y) not in map_matrix:
            map_matrix.append((x, y))
    return map_matrix