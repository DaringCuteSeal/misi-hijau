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

from core.sprite_classes import TilemapBasedSprite
from core.game_handler import GameHandler
from core.common import MineralType, Sfx, SoundType, ProgressStatusbarItem, BLANK_UV, MAP_Y_OFFSET_TILES, Icon
from game import events

class MineralsHandler(TilemapBasedSprite):

    costumes = {
        "mineral_1": (1, 2),
        "mineral_2": (1, 3),
        "mineral_3": (0, 3)
    }

    minerals_icon = [
        Icon(0, 8, 96, 8, 8),
        Icon(0, 0, 104, 8, 8),
        Icon(0, 8, 104, 8, 8)
    ]

    soundbank = {
        "mineral_increment": Sfx(SoundType.AUDIO, 1, 12)
    }

    def __init__(self, game_handler: GameHandler):
        self.minerals_progressbar = ProgressStatusbarItem(1, 0, self.get_minerals_count, pyxel.COLOR_WHITE, 0, 75, 10, self.minerals_icon[0], "Mineral", pyxel.COLOR_WHITE)

        self.statusbar_items = [
            self.minerals_progressbar
        ]

        self.mineral_coordinates_list: list[tuple[int, int]] = []
        self.game_handler = game_handler
        self.game_handler.game_components.event_handler.add_handler(events.TilemapPlayerCheck.name, self.player_collision_check_handler)
        self.setup()
        self._reset_progressbar()
    
    def setup(self):
        self.collected_minerals = 0
        self.level = self.game_handler.levelhandler.get_curr_lvl()
        self.minerals_progressbar.icon = self.minerals_icon[self.level.idx - 1]
        self.game_handler.game_components.event_handler.trigger_event(events.UpdateStatusbar)
        mineral_type = self.level.mineral_type
        match mineral_type:
            case MineralType.MINERAL_1:
                self.mineral_costume = self.costumes["mineral_1"]
            case MineralType.MINERAL_2:
                self.mineral_costume = self.costumes["mineral_2"]
            case MineralType.MINERAL_3:
                self.mineral_costume = self.costumes["mineral_3"]
        self.spawn()

    def _reset_progressbar(self):
        self.minerals_progressbar.progress_col = self.level.minerals_statusbar_color
        self.minerals_progressbar.new_max_val(self.level.minerals_count)

    def spawn(self):
        """
        Spawn the minerals in random coordinates, the max minerals count is set by the level's `max_minerals` attribute.
        """
        self._clean_grid()
        self.mineral_coordinates_list = self._generate_random_mimerals_map_matrix(self.level.minerals_count, self.level.levelmap.level_width, self.level.levelmap.level_height, self.level.levelmap.map_x, self.level.levelmap.map_y)
        for x, y in self.mineral_coordinates_list:
            pyxel.tilemap(0).pset(x, y, self.mineral_costume)
    
    def _clean_grid(self):
        for x, y in self.mineral_coordinates_list:
            pyxel.tilemap(0).pset(x, y, BLANK_UV) 

    def _generate_random_mimerals_map_matrix(self, num_tiles: int, map_w: int, map_h: int, map_x: int, map_y: int) -> list[tuple[int, int]]:
        """
        Generate a random map matrix: an array containing tuples of coordinates. `w` and `h` is in tilemap scale.
        """
        map_matrix: list[tuple[int, int]] = []
        while len(map_matrix) < num_tiles:
            # The extra 3 offset is needed so the player can *actually* collect the item. Also is just a nice padding.
            x = pyxel.rndi(3, map_w - 3) + map_x
            y = pyxel.rndi(3, map_h - 3) + MAP_Y_OFFSET_TILES + map_y
            if (x, y) not in map_matrix:
                map_matrix.append((x, y))
        return map_matrix

    def restart_level(self):
        self.collected_minerals = 0
        self.spawn()
    
    def init_level(self):
        self.setup()
        self._reset_progressbar()

    def player_collision_check_handler(self, uv: tuple[int, int], tile_x: int, tile_y: int) -> bool:
        if uv == (self.mineral_costume):
            self.collected_minerals += 1
            if self.collected_minerals == self.level.minerals_count:
                self.level.minerals_all_collected = True
                self.game_handler.game_components.event_handler.trigger_event(events.CheckLevelComplete)
                self.minerals_progressbar.progress_col = pyxel.COLOR_GREEN

            self.game_handler.game_components.event_handler.trigger_event(events.UpdateStatusbar)
            self.game_handler.game_components.soundplayer.play(self.soundbank["mineral_increment"])
            pyxel.tilemap(0).pset(tile_x, tile_y, BLANK_UV)
            return True
        return False
    
    # Functions for statusbar
    def get_minerals_count(self) -> int:
        return self.collected_minerals