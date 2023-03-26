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
from ..components import ALPHA_COL, GameStateManager, Sfx, SoundType, tile_to_real
from ..utils import Ticker
from . import Sprite, SpriteCoordinate, player, bullets, is_colliding

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
        self.is_dead = False

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

    def __init__(self, x_map: float, y_map: float, level_height: int, level_width: int):
        self.coord = SpriteCoordinate(-20, -20, -20, -20)
        self.coord.x_map = x_map
        self.coord.y_map = y_map
        self.level_height = level_height
        self.level_width = level_width
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

class EnemyGroup(Sprite):
    def __init__(self, enemy_type: EnemyType, game: GameStateManager, player: player.Player, bullets: bullets.Bullets): # TODO: players collision detection
        self.type = enemy_type
        level = game.levelhandler.get_curr()
        self.map = level.levelmap.enemies_map
        self.camera = game.camera
        self.soundplayer = game.soundplayer
        self.bullets = bullets
        self.level_height = tile_to_real(level.levelmap.level_height)
        self.level_width = tile_to_real(level.levelmap.level_width)
        self.enemies: list[EnemyEntity] = []
        self.spawn()
        self.soundbank = {
            "explode": Sfx(SoundType.AUDIO, 0, 11)
        }


    def spawn(self):
        """
        Spawn all enemies based on the enemy map.
        """
        for x, y in self.map:
            x = tile_to_real(x)
            y = tile_to_real(y)
            match self.type:
                case EnemyType.ENEMY_1:
                    self.enemies.append(EnemyGrug(x, y, self.level_height, self.level_width))
                case EnemyType.ENEMY_2:
                    self.enemies.append(EnemyPhong(x, y))
                case EnemyType.ENEMY_3:
                    self.enemies.append(EnemySquidge(x, y))
    
    def update(self):
        for enemy in self.enemies:
            enemy.map_to_view(self.camera.y)
            enemy.update()

            for bullet in self.bullets.bullets:
                if is_colliding(bullet, enemy):
                    enemy.is_dead = True
                    self.enemies.remove(enemy)
                    bullet.is_dead = True
                    self.bullets.bullets.remove(bullet)
                    self.soundplayer.play(self.soundbank["explode"])
                    
    def draw(self):
        for enemy in self.enemies:
            if enemy.is_sprite_in_viewport():
                enemy.draw()
    
    def reset(self):
        self.enemies = []
        self.spawn()

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

   
    