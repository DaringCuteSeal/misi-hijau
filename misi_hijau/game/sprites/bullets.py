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

from core.common import Sfx, SoundType, WINDOW_HEIGHT
from core.sprite_classes import Sprite, SpriteCoordinate, SpriteHandler
from core.game_handler import GameHandler
from core.utils import tile_to_real
from game import events

class Bullet(Sprite):

    def __init__(self, coord: SpriteCoordinate, color: int, y_speed: float = 3, x_speed: float = 0, width: int = 2, height: int = 8, from_enemy: bool = False):
        self.coord = coord
        self.color = color
        self.is_dead = False
        self.y_speed = y_speed
        self.x_speed = x_speed
        self.from_enemy = from_enemy
        self.w = width
        self.h = height
    
    def update(self):
        self.coord.y_map -= self.y_speed
        self.coord.x_map -= self.x_speed

    def draw(self):
        if self.is_sprite_in_viewport():
            pyxel.rect(self.coord.x, self.coord.y, self.w, self.h, self.color)
    
class BulletsHandler(SpriteHandler):
    def __init__(self, game_handler: GameHandler):
        self.bullets: list[Bullet] = []
        self.game_handler = game_handler
        self.game_handler.game_components.event_handler.add_handler(events.PlayerShootBullets.name, self.player_shoot_handler)
        self.game_handler.game_components.event_handler.add_handler(events.SquidgeShootBullet.name, self.squidge_shoot_handler)
        self.game_handler.game_components.event_handler.add_handler(events.EnemiesBulletsCheck.name, self.bullets_colliding_enemy_check_handler)
        self.game_handler.game_components.event_handler.add_handler(events.PlayerBulletsCheck.name, self.bullets_colliding_player_check_handler)
        self.soundbank = {
            "explode": Sfx(SoundType.AUDIO, 1, 11)
        }
        self.setup()
    
    def setup(self):
        level = self.game_handler.levelhandler.get_curr_lvl()
        self.level_height = tile_to_real(level.levelmap.level_height)
        self.level_width = tile_to_real(level.levelmap.level_width)
        self.bullet_color = level.bullet_color

    def append_bullet(self, x: float, y: float, color: int, y_speed: float = 3, x_speed: float = 0, width: int = 2, height: int = 8, from_enemy: bool = False):
        bullet = Bullet(SpriteCoordinate(-30, -30, x, y), color, y_speed, x_speed, width, height, from_enemy)
        bullet.map_to_view(self.game_handler.game_components.camera.y)
        self.bullets.append(bullet)

    def update(self):
        if len(self.bullets) <= 0:
            return
        
        for bullet in self.bullets:
            bullet.update()
            bullet.map_to_view(self.game_handler.game_components.camera.y)

            # XXX at this point I just realized that I can 
            # make an if_touching_level_edge method for the Sprite class
            if (
                bullet.coord.y_map > self.level_height
                    or bullet.coord.y_map < 0
                    or bullet.coord.x_map > self.level_width
                    or bullet.coord.x_map < 0
            ):
                self.bullets.remove(bullet)

            bullet.map_to_view(self.game_handler.game_components.camera.y)

    def draw(self):
        if len(self.bullets) <= 0:
            return
        
        for bullet in self.bullets:
            bullet.draw()
    
    def player_shoot_handler(self, player_x: float, player_y: float):
        self.append_bullet(player_x + 7, player_y - 8, self.bullet_color, 3) # FIXME or maybe not, idk too lazy: add w and h as parameter
    
    def squidge_shoot_handler(self, x_enemy: float, y_enemy: float, x_player: float, y_player: float):
        if len([bullet for bullet in self.bullets if bullet.from_enemy]) > 5:
            return

        # credit: chatgpt because I'm a not-so-special 8th grader :sunglasses:
        dx = x_enemy - x_player
        dy = y_enemy - y_player
        angle_rad = pyxel.atan2(dy, dx) # get angle
        # calculate the x and y components of the angle
        x_component = pyxel.cos(angle_rad)
        y_component = pyxel.sin(angle_rad)
        self.append_bullet(x_enemy, y_enemy, pyxel.COLOR_YELLOW, y_component, x_component, 2, 2, True)

    # FIXME: DOUBLE FOR LOOPS. IDC, IT'S 8 PM AND I NEED TO FINISH THIS OFF ^_^
    # FIXME: also very inconsistent name, thank you
    def bullets_colliding_player_check_handler(self, x_player: float, y_player: float, w_player: int, h_player: int):
        for bullet in self.bullets:
            if not bullet.from_enemy:
                continue

            if bullet.is_colliding(x_player, y_player, w_player, h_player):
                if self.game_handler.game_components.event_handler.trigger_event(events.DecreasePlayerHealth(-1)):
                    self.bullets.remove(bullet) if bullet in self.bullets else None

    def bullets_colliding_enemy_check_handler(self, enemy_x_map: float, enemy_y_map: float, enemy_w: int, enemy_h: int) -> bool:
        if len(self.bullets) <= 0: # Only check collision if there are actually bullets to check for.
            return False
        
        for bullet in self.bullets:
            if bullet.from_enemy:
                continue

            # Calculate the viewport coordinates because we always use viewport coords for
            # collision detection...
            # XXX kinda clunky, make the collision detection use map coords directly if needed.
            x = enemy_x_map
            y = enemy_y_map - self.game_handler.game_components.camera.y + WINDOW_HEIGHT // 2

            if bullet.is_colliding(x, y, enemy_w, enemy_h):
                self.bullets.remove(bullet) if bullet in self.bullets else None
                self.game_handler.game_components.event_handler.trigger_event(events.AppendBlastEffect(enemy_x_map, enemy_y_map, enemy_w, enemy_h))
                self.game_handler.game_components.soundplayer.play(self.soundbank["explode"])
                self.game_handler.game_components.event_handler.trigger_event(events.UpdateStatusbar)
                return True
        return False
    
    def restart_level(self):
        self.bullets = []
    
    def init_level(self):
        self.setup()