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
from enum import Enum
from ..common import ALPHA_COL, Level, BLANK_UV, MAP_Y_OFFSET_TILES, StatusbarItem
from ..utils import Ticker, tile_to_real
from . import Sprite, SpriteCoordinate
from ..game_handler import GameComponents
from .. import events

ENEMY_SPAWNER_UV = (7, 1)

class EnemyType(Enum):
    ENEMY_1 = 0 # Krelth/Grug
    ENEMY_2 = 1 # Naxor/Phong
    ENEMY_3 = 2 # Octyca/Squidge

class EnemyEntity(Sprite):
    keybindings = {}
    soundbank = {}
    costumes = {}

    def __init__(self, x_map: float, y_map: float):
        self.coord = SpriteCoordinate()
        self.coord.x_map = x_map
        self.coord.y_map = y_map

    def draw(self):
        pyxel.blt(self.coord.x, self.coord.y, self.img, self.u, self.v, self.w, self.h, ALPHA_COL)
    
    def update(self):
        pass

    def reset(self):
        pass

class EnemyGrug(EnemyEntity):
    u = 0
    v = 48
    health = 2

    def __init__(self, x_map: float, y_map: float, level: Level):
        self.coord = SpriteCoordinate(-20, -20, -20, -20)
        self.coord.x_map = x_map
        self.coord.y_map = y_map
        self.level_height = tile_to_real(level.levelmap.level_height)
        self.level_width = tile_to_real(level.levelmap.level_width)
        self.ticker = Ticker(8)

    def update(self):
        self.ticker.update()
        if self.ticker.get():
            self.coord.x_map += pyxel.rndf(-2, 2)
            self.coord.y_map += pyxel.rndf(-2, 2)
            if self.coord.x_map > self.level_width: 
                self.coord.x_map = self.level_width - 2
            if self.coord.x_map < 0:
                self.coord.x_map = 0
            if self.coord.y_map > self.level_height:
                self.coord.y_map = self.level_height

    
class EnemyPhong(EnemyEntity):
    u = 8
    v = 48
    health = 4

    def update(self):
        pass

class EnemySquidge(EnemyEntity):
    u = 0
    v = 56
    health = 8

    def update(self):
        pass

class EnemyHandler(Sprite):
    def __init__(self, level: Level, enemy_type: EnemyType, game: GameComponents):
        self.enemies_coordinates_list: list[tuple[int, int]] = []
        self.enemy_type = enemy_type
        self.game = game
        self.level = level
        self.levelmap = level.levelmap
        self.enemies: list[EnemyEntity] = []
        self.enemies_coordinates_list = self.get_enemies_matrix()
        self.game.statusbar.add(StatusbarItem(2, self.get_enemy_count, pyxel.COLOR_WHITE, 2))

    def get_enemies_matrix(self) -> list[tuple[int, int]]:
        """
        Get a list of enemy coordinates.
        It works by checking each tile in the map and compares it to the current enemy type's UV coordinates.
        """
        enemies_matrix: list[tuple[int, int]] = []
        tilemap = pyxel.tilemap(0)
        for y in range(self.levelmap.map_y + MAP_Y_OFFSET_TILES, self.levelmap.map_y + MAP_Y_OFFSET_TILES +  self.levelmap.level_height):
            for x in range(self.levelmap.map_x, self.levelmap.map_x + self.levelmap.level_width):
                tile_type = tilemap.pget(x, y)
                if tile_type == ENEMY_SPAWNER_UV:
                    enemies_matrix.append((x, y))
        return enemies_matrix

    def spawn(self):
        """
        Spawn all enemies based on the the tilemap. 
        """
        self.clear_enemies_spawnpoints()
        [self._append_enemy(self.enemy_type, x, y) for x, y in self.enemies_coordinates_list]
            
    def clear_enemies_spawnpoints(self):
        """
        Reset all spawn points. Turns all spawn point tiles to blank tiles.
        """
        tilemap = pyxel.tilemap(0)
        [tilemap.pset(x, y, BLANK_UV) for x, y in self.enemies_coordinates_list]
    
    def _append_enemy(self, enemy_type: EnemyType, x: int, y: int):

        x = tile_to_real(x)
        y = tile_to_real(y - MAP_Y_OFFSET_TILES)
        match enemy_type:
            case EnemyType.ENEMY_1:
                enemy = EnemyGrug(x, y, self.level)
            case EnemyType.ENEMY_2:
                enemy = EnemyPhong(x, y)
            case EnemyType.ENEMY_3:
                enemy = EnemySquidge(x, y)
        self.enemies.append(enemy)

    def update(self):
        for enemy in self.enemies:
            enemy.map_to_view(self.game.camera.y)
            enemy.update()

            # XXX try checking collision on individual sprite update instead (without the EnemiesHandler)
            # also maybe this can mean the enemy will only need to trigger one event and then the player can also have a handler
            if self.game.event_handler.trigger_event(events.BulletsCheck(enemy.coord.x, enemy.coord.y, enemy.w, enemy.h)):
                self.enemies.remove(enemy)
            
            if self.game.event_handler.trigger_event(events.PlayerCollidingEnemy(enemy.coord.x, enemy.coord.y, enemy.w, enemy.h)):
                self.reset_handler()
                    
    def draw(self):
        for enemy in self.enemies:
            if enemy.is_sprite_in_viewport():
                enemy.draw()
    
    def reset_handler(self):
        self.enemies = []
        self.spawn()

    def get_enemy_count(self) -> str:
        return ""
#   for enemy in enemies:
#       for bullet in bullets:
#           if (
#               enemy.x + enemy.w > bullet.x
#               and bullet.x + bullet.w > enemy.x
#               and enemy.y + enemy.h > bullet.y
#               and bullet.y + bullet.h > enemy.y
#           ):
#               enemy.is_alive = False
#               bullet.is_alive = False
#               blasts.append(
#                   Blast(enemy.x + ENEMY_WIDTH / 2, enemy.y + ENEMY_HEIGHT / 2)
#               )

   
    