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
from ..game_handler import GameComponents
from .. import events
from ..common import MineralType, Sfx, SoundType, StatusbarItem, Level, BLANK_UV, MAP_Y_OFFSET_TILES
from ..utils import real_to_tile
import pyxel

class MineralHandler(Sprite):
    minerals_grid = []

    costumes = {
        "mineral_1": (1, 2),
        "mineral_2": (1, 3),
        "mineral_3": (0, 3)
    }

    soundbank = {
        "mineral_increment": Sfx(SoundType.AUDIO, 2, 12)
    }

    def __init__(self, level: Level, game: GameComponents):
        self.game = game
        self.game.event_handler.add_handler(events.MineralsCheck.name, self.player_collision_check_handler)
        self.game.event_handler.add_handler(events.LevelRestart.name, self.reset_handler)
        self.game.statusbar.add(StatusbarItem(1, self.get_minerals_count, pyxel.COLOR_WHITE))

        self.collected_minerals = 0
        self.level = level
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

    def spawn(self):
        """
        Spawn the minerals in random coordinates, the max minerals count is set by the level's `max_minerals` attribute.
        """
        self._clean_grid()
        self.minerals_grid = self._generate_random_map_matrix(self.level.max_minerals, self.level.levelmap.level_width, self.level.levelmap.level_height, self.level.levelmap.map_x, self.level.levelmap.map_y)
        for x, y in self.minerals_grid:
            pyxel.tilemap(0).pset(x, y, self.mineral_costume)
    
    def _clean_grid(self):
        for x, y in self.minerals_grid:
            pyxel.tilemap(0).pset(x, y,BLANK_UV) 


    def _generate_random_map_matrix(self, num_tiles: int, map_w: int, map_h: int, map_x: int, map_y: int) -> list[tuple[int, int]]:
        """
        Generate a random map matrix: an array containing tuples of coordinates. `w` and `h` is in tilemap scale.
        """
        map_matrix: list[tuple[int, int]] = []
        while len(map_matrix) < num_tiles:
            # The extra 1 offset is needed so the player can *actually* collect the item. Also is just a nice padding.
            x = pyxel.rndi(pyxel.TILE_SIZE + 1, map_w - 1) + map_x
            y = pyxel.rndi(MAP_Y_OFFSET_TILES + 1, map_h - 1) + map_y # the map is offset by 16 tiles
            if (x, y) not in map_matrix:
                map_matrix.append((x, y))
        return map_matrix

    def reset_handler(self):
        self.collected_minerals = 0
        self.spawn()

    def player_collision_check_handler(self, player_x_map: float, player_y_map: float, player_h: int) -> bool:
        # +1 tile here to center the player coordinate.

        x = real_to_tile(player_x_map) + self.level.levelmap.map_x + 1
        y = real_to_tile(player_y_map) + self.level.levelmap.map_y + 1 + MAP_Y_OFFSET_TILES

        tilemap = pyxel.tilemap(0).pget(x, y)
        if tilemap == (self.mineral_costume):
            self.collected_minerals += 1
            self.game.event_handler.trigger_event(events.UpdateStatusbar)
            self.game.soundplayer.play(self.soundbank["mineral_increment"])
            pyxel.tilemap(0).pset(x, y, BLANK_UV)
            return True
        return False
    
    # Functions for statusbar
    def get_minerals_count(self) -> str:
        return f"Minerals collected: {self.collected_minerals:>2} / {self.level.max_minerals}"