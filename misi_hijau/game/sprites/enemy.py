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
from abc import abstractmethod
from core.components import EventHandler
from core.common import ALPHA_COL, Level, BLANK_UV, MAP_Y_OFFSET_TILES, ProgressStatusbarItem, EnemyType, Icon, TickerItem, Sfx, SoundType
from core.utils import tile_to_real
from core.sprite_classes import Sprite, SpriteCoordinate, SpriteHandler
from core.game_handler import GameHandler
from game import events

ENEMY_SPAWNER_UV = (7, 1)

class EnemyEntity(Sprite):
    health: int = 1

    def __init__(self, x_map: float, y_map: float):
        self.coord = SpriteCoordinate()
        self.coord.x_map = x_map
        self.coord.y_map = y_map

    def draw(self):
        pyxel.blt(self.coord.x, self.coord.y, self.img, self.u, self.v, self.w, self.h, ALPHA_COL)
    
    @abstractmethod
    def check_deletion(self) -> bool:
        pass

    @abstractmethod
    def update(self):
        pass

class EnemyGrug(EnemyEntity):
    u = 0
    v = 48
    w = 8
    h = 8
    health = 1

    def __init__(self, x_map: float, y_map: float, level: Level, ticker: TickerItem):
        self.coord = SpriteCoordinate(-20, -20, -20, -20)
        self.coord.x_map = x_map
        self.coord.y_map = y_map
        self.level_height = tile_to_real(level.levelmap.level_height)
        self.level_width = tile_to_real(level.levelmap.level_width)
        self.update_ticker = ticker

    def update(self):
        if self.update_ticker.get():
            self.coord.x_map += pyxel.rndf(-2, 2)
            self.coord.y_map += pyxel.rndf(-2, 2)
            if self.coord.x_map > self.level_width:
                self.coord.x_map = self.level_width - 2
            if self.coord.x_map < 0:
                self.coord.x_map = 0
            if self.coord.y_map > self.level_height:
                self.coord.y_map = self.level_height
        
    def check_deletion(self) -> bool:
        return self.health == 0
    
class EnemyPhong(EnemyEntity):
    u = 8
    v = 48
    health = 2

    def __init__(self, x_map: float, y_map: float, level: Level, ticker: TickerItem):
        self.coord = SpriteCoordinate(-20, -20, -20, -20)
        self.coord.x_map = x_map
        self.coord.y_map = y_map
        self.level_height = tile_to_real(level.levelmap.level_height)
        self.level_width = tile_to_real(level.levelmap.level_width)
        self.direction_x = pyxel.rndf(-2.5, 3)
        self.direction_y = pyxel.rndf(1, 4)
        self.update_ticker = ticker

    def update(self):
        if not self.update_ticker.get():
            return

        if self.coord.x_map < 0:
            self.coord.x_map = 1
            self.direction_x *= -1
        if self.coord.x_map > self.level_width - self.w:
            self.coord.x_map = self.level_width - self.w - 1
            self.direction_x *= -1
        if self.coord.y_map > self.level_height - self.h:
            self.direction_y *= -1
            self.coord.y_map = self.level_height - self.h - 1
        if self.coord.y_map < 0:
            self.direction_y *= -1
            self.coord.y_map = 1

        self.coord.x_map += self.direction_x + pyxel.rndf(-2, 2)
        self.coord.y_map += self.direction_y + pyxel.rndf(-2, 2)

    def check_deletion(self) -> bool:
        return self.health == 0
    
class EnemySquidge(EnemyEntity):
    u = 0
    v = 56
    health = 3

    def __init__(self, x_map: float, y_map: float, level: Level, ticker: TickerItem, shoot_ticker: TickerItem):
        self.coord = SpriteCoordinate(-20, -20, -20, -20)
        self.coord.x_map = x_map
        self.coord.y_map = y_map
        self.update_ticker = ticker
        self.shoot_ticker = shoot_ticker
        self.level_height = tile_to_real(level.levelmap.level_height)
        self.level_width = tile_to_real(level.levelmap.level_width)
        self.direction_x = pyxel.rndf(-0.8, 0.8)
        self.direction_y = pyxel.rndf(-1, 1)

    def update(self):
        if not self.update_ticker.get():
            return

        if self.coord.x_map < 0:
            self.coord.x_map = 1
            self.direction_x *= -1
        if self.coord.x_map > self.level_width - self.w:
            self.coord.x_map = self.level_width - self.w - 1
            self.direction_x *= -1
        if self.coord.y_map > self.level_height - self.h:
            self.direction_y *= -1
            self.coord.y_map = self.level_height - self.h - 1
        if self.coord.y_map < 0:
            self.direction_y *= -1
            self.coord.y_map = 1

        self.coord.x_map += self.direction_x + pyxel.rndf(-1, 1)
        self.coord.y_map += self.direction_y + pyxel.rndf(-1, 1)


    def check_deletion(self) -> bool:
        return self.health == 0
    
    def check_shoot(self, event_handler: EventHandler):
        event_handler.trigger_event(events.SquidgeNearPlayer(self.coord.x_map, self.coord.y_map, self.w, self.h)) if self.shoot_ticker.get() else None

class EnemyHandler(SpriteHandler):

    enemies_icon = [
        Icon(0, 16, 96, 8, 8),
        Icon(0, 24, 96, 8, 8),
        Icon(0, 16, 104, 8, 8)
    ]

    soundbank = {
        "attacked": Sfx(SoundType.AUDIO, 0, 21)
    }

    def __init__(self, game_handler: GameHandler):
        self.game_handler = game_handler
        self.enemies_ticker = self.game_handler.game_components.ticker.attach(8)
        self.game_components = game_handler.game_components
        self.enemy_coordinates_list: list[tuple[int, int]] = []
        self.enemies: list[EnemyEntity] = []
        self.enemies_hit_progressbar = ProgressStatusbarItem(2, 1, self.get_enemies_eliminated_count, pyxel.COLOR_WHITE, 0, 75, 10, self.enemies_icon[0], "Alien", pyxel.COLOR_WHITE)
        self.setup()
        self._reset_progressbar()
        self.game_components.event_handler.add_handler(events.ActivateLevel.name, self._activate_enemy)

        self.statusbar_items = [
            self.enemies_hit_progressbar
        ]

    def setup(self):
        self.level = self.game_handler.levelhandler.get_curr_lvl()
        self.levelmap = self.level.levelmap
        self.enemy_type = self.level.enemy_type
        self.enemies_eliminated = 0
        self.enemy_coordinates_list = self._generate_enemies_matrix()
        self.enemies_hit_progressbar.icon = self.enemies_icon[self.level.idx - 1]
        self.spawn()
        self.update_enemies = False

    def _reset_progressbar(self):
        self.enemies_hit_progressbar.progress_col = self.level.enemies_statusbar_color
        self.enemies_hit_progressbar.new_max_val(self.enemies_count)

    def _generate_enemies_matrix(self) -> list[tuple[int, int]]:
        """
        Get an array of enemy coordinates.
        It works by checking each tile in the map and compares it to the current enemy type's UV coordinates.
        """
        # The coordinates in this list are the _actual_ coordinates on the entire tilemap, not the game map coordinates.
        enemies_matrix: list[tuple[int, int]] = []
        tilemap = pyxel.tilemap(0)
        for y in range(self.levelmap.map_y + MAP_Y_OFFSET_TILES, self.levelmap.map_y + MAP_Y_OFFSET_TILES +  self.levelmap.level_height):
            for x in range(self.levelmap.map_x, self.levelmap.map_x + self.levelmap.level_width):
                if tilemap.pget(x, y) == ENEMY_SPAWNER_UV:
                    enemies_matrix.append((x, y))
        self.enemies_count = len(enemies_matrix)
        self.game_components.event_handler.trigger_event(events.BroadcastEnemiesCount(self.enemies_count))
        return enemies_matrix

    def spawn(self):
        """
        Spawn all enemies based on the the tilemap. 
        """
        self.clear_enemies_spawnpoints()
        for x, y in self.enemy_coordinates_list:
            self._append_enemy(self.enemy_type, x + pyxel.rndf(-1, 1), y + pyxel.rndf(-1, 1))
            
    def clear_enemies_spawnpoints(self):
        """
        Reset all spawn points. Turns all spawn point tiles to blank tiles.
        """
        tilemap = pyxel.tilemap(0)
        [tilemap.pset(x, y, BLANK_UV) for x, y in self.enemy_coordinates_list]
    
    def _append_enemy(self, enemy_type: EnemyType, x: int, y: int):

        x = tile_to_real(x - self.levelmap.map_x)
        y = tile_to_real(y - MAP_Y_OFFSET_TILES - self.levelmap.map_y)
        match enemy_type:
            case EnemyType.ENEMY_1:
                enemy = EnemyGrug(x, y, self.level, self.game_components.ticker.attach(pyxel.rndi(4, 8)))
            case EnemyType.ENEMY_2:
                enemy = EnemyPhong(x, y, self.level, self.game_components.ticker.attach(pyxel.rndi(4, 8)))
            case EnemyType.ENEMY_3:
                enemy = EnemySquidge(x, y, self.level, self.game_components.ticker.attach(pyxel.rndi(6, 10)), self.game_components.ticker.attach(15))
        self.enemies.append(enemy)

    def _activate_enemy(self):
        self.update_enemies = True

    def update(self):
        for enemy in self.enemies:
            enemy.map_to_view(self.game_components.camera.y)
            # XXX try checking collision on individual sprite update instead (without the EnemiesHandler)
            # also maybe this can mean the enemy will only need to trigger one event and then the player can also have a handler
            if isinstance(enemy, EnemySquidge):
                enemy.check_shoot(self.game_components.event_handler)

            if enemy.is_sprite_in_viewport() and not self.level.enemies_all_eliminated:
                if self.game_components.event_handler.trigger_event(events.EnemiesBulletsCheck(enemy.coord.x_map, enemy.coord.y_map, enemy.w, enemy.h)):
                    enemy.health -= 1
                    if enemy.check_deletion():
                        self.enemies.remove(enemy)
                        self.game_components.soundplayer.play(self.soundbank["attacked"])
                        self.enemies_eliminated += 1
                        self.game_components.event_handler.trigger_event(events.UpdateStatusbar)
                        if self.enemies_eliminated == self.enemies_count:
                            self.level.enemies_all_eliminated = True
                            self.enemies_hit_progressbar.progress_col = pyxel.COLOR_GREEN
                            self.game_components.event_handler.trigger_event(events.CheckLevelComplete)
                
                self.game_components.event_handler.trigger_event(events.PlayerCollidingEnemy(enemy.coord.x, enemy.coord.y, enemy.w, enemy.h))

            enemy.update() if self.update_enemies else None

    def draw(self):
        for enemy in self.enemies:
            if enemy.is_sprite_in_viewport():
                enemy.draw()
    
    def init_level(self):
        self.enemies = []
        self.setup()
        self._reset_progressbar()

    def restart_level(self):
        self.update_enemies = None
        self.enemies = []
        self.enemies_eliminated = 0
        self.spawn()

    def get_enemies_eliminated_count(self) -> int:
        return self.enemies_eliminated