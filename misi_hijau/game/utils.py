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

# def check_tilemap_uv(x: float, y: float, levelmap_x: int, levelmap_y: int) -> tuple[int, int]:
#     """
#     Return U,V of a tile from the level map's `x` and `y`.
#     """
#     # +1 tile here to center the player coordinate.

#     x = real_to_tile(x) + self.level.levelmap.map_x + 1
#     y = real_to_tile(y) + self.level.levelmap.map_y + 1 + MAP_Y_OFFSET_TILES

#     tilemap = pyxel.tilemap(0).pget(x, y)
#     if tilemap == (self.mineral_costume):
#         self.collected_minerals += 1
#         if self.collected_minerals == self.level.max_minerals:
#             self.level.minerals_all_collected = True
#             self.game.event_handler.trigger_event(events.CheckLevelComplete)

#         self.game.event_handler.trigger_event(events.UpdateStatusbar)
#         self.game.soundplayer.play(self.soundbank["mineral_increment"])
#         pyxel.tilemap(0).pset(x, y, BLANK_UV)
#         return True
#     return False