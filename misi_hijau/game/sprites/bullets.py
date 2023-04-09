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

from ..common import Sfx, SoundType, WINDOW_HEIGHT
from . import Sprite, SpriteCoordinate, SpriteHandler
from ..game_handler import GameHandler
from .. import events
import pyxel

class Bullet(Sprite):
    w = 2
    h = 8
    speed = 3
    # uh why do i need to add these...
    keybindings = {}
    costumes = {}
    soundbank = {}

    def __init__(self, coord: SpriteCoordinate, color: int):
        self.coord = coord
        self.color = color
        self.is_dead = False
    
    def update(self):
        pass

    def draw(self):
        if self.is_sprite_in_viewport():
            pyxel.rect(self.coord.x, self.coord.y, self.w, self.h, self.color)
    

class BulletsHandler(SpriteHandler):
    def __init__(self, game_handler: GameHandler):
        self.bullets: list[Bullet] = []
        self.game_handler = game_handler
        self.game_handler.game_components.event_handler.add_handler(events.PlayerShootBullets.name, self.shoot_handler)
        self.game_handler.game_components.event_handler.add_handler(events.BulletsCheck.name, self.bullets_colliding_check_handler)
        self.soundbank = {
            "explode": Sfx(SoundType.AUDIO, 2, 11)
        }
        self.setup()
    
    def setup(self):
        level = self.game_handler.levelhandler.get_curr_lvl()
        self.bullet_color = level.bullet_color

    def append_bullet(self, x: float, y: float, color: int):
        bullet = Bullet(SpriteCoordinate(-30, -30, x, y), color)
        self.bullets.append(bullet)

    def update(self):
        if len(self.bullets) > 0:
            for bullet in self.bullets:
                bullet.map_to_view(self.game_handler.game_components.camera.y)
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
    
    def shoot_handler(self, player_x: float, player_y: float):
        self.append_bullet(player_x + 7, player_y - 8, self.bullet_color)

    def bullets_colliding_check_handler(self, enemy_x_map: float, enemy_y_map: float, enemy_w: int, enemy_h: int) -> bool:
        if len(self.bullets) > 0: # Only check collision if there are actually bullets to check for.
            for bullet in self.bullets:

                # Calculate the viewport coordinates because we always use viewport coords for
                # collision detection...
                # XXX kinda clunky, make the collision detection use map coords directly if needed.
                x = enemy_x_map
                y = enemy_y_map - self.game_handler.game_components.camera.y + WINDOW_HEIGHT // 2

                if bullet.is_colliding(x, y, enemy_w, enemy_h):

                    self.bullets.remove(bullet)
                    self.game_handler.game_components.event_handler.trigger_event(events.AppendBlastEffect(enemy_x_map, enemy_y_map, enemy_w, enemy_h))
                    self.game_handler.game_components.soundplayer.play(self.soundbank["explode"])
                    self.game_handler.game_components.event_handler.trigger_event(events.UpdateStatusbar)
                    return True
        return False
    
    def restart_level(self):
        self.bullets = []
    
    def init_level(self):
        self.setup()
    
    # Functions for statusbar