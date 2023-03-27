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

from ..common import Sfx, SoundType
from . import Sprite, SpriteCoordinate
from ..handler import GameStateManager
import pyxel

class Bullet(Sprite):
    w = 2
    h = 8
    speed = 3
    # uh why do i need to add these...
    keybindings = {}
    costumes = {}
    soundbank = {}

    def __init__(self, coord: SpriteCoordinate, color: int, game: GameStateManager):
        self.coord = coord
        self.color = color
        self.camera = game.camera
        self.is_dead = False
    
    def update(self):
        self.map_to_view(self.camera.y)

    def draw(self):
        if self.is_sprite_in_viewport():
            pyxel.rect(self.coord.x, self.coord.y, self.w, self.h, self.color)
    

class Bullets(Sprite):
    def __init__(self, game: GameStateManager):
        self.bullets: list[Bullet] = []
        self.game = game
        self.bullet_color = self.game.level_handler.get_curr().bullet_color
        self.game.event_handler.add_handler("player_shoot_bullets", self.shoot_handler)
        self.game.event_handler.add_handler("bullets_check", self.bullets_colliding_check_handler)
        self.soundbank = {
            "explode": Sfx(SoundType.AUDIO, 0, 11)
        }
    
    def append(self, x: float, y: float, color: int):
        bullet = Bullet(SpriteCoordinate(-30, -30, x, y), color, self.game)
        self.bullets.append(bullet)

    def update(self):
        if len(self.bullets) > 0:
            for bullet in self.bullets:
                bullet.coord.y_map -= bullet.speed
                bullet.update()
                if bullet.coord.y_map < 0 or bullet.coord.y + bullet.h - 1 < 0:
                        bullet.is_dead = True

                if bullet.is_dead:
                    self.bullets.remove(bullet)


    def draw(self):
        if len(self.bullets) > 0:
            for bullet in self.bullets:
                bullet.draw()
    
    def reset(self):
        self.bullets = []
  
    def shoot_handler(self, player_x: float, player_y: float):
        self.append(player_x + 7, player_y - 8, self.bullet_color)

    def bullets_colliding_check_handler(self, enemy_x: float, enemy_y: float, enemy_w: float, enemy_h: float) -> bool:
        for bullet in self.bullets:
            if bullet.is_colliding(enemy_x, enemy_y, enemy_w, enemy_h):
                self.bullets.remove(bullet)
                self.game.soundplayer.play(self.soundbank["explode"])
                return True
        return False