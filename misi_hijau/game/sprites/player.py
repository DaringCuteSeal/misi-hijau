# Copyright 2023 Cikitta Tjok

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from dataclasses import dataclass
import pyxel
from enum import Enum
from math import sqrt # pyxel.sqrt(0) returns denormalized number; we need it to return 0.
from . import Sprite, SpriteCoordinate
from .stars import Stars
from ..base import (
    ALPHA_COL,
    WINDOW_HEIGHT,
    Direction,
    GameStateManager,
    KeyFunc,
    PlayerShip,
    Sfx,
    SoundType,
    Ticker,
    Camera,
    KeyTypes,
    StatusbarItem,
    tile_to_real 
)
    
class PlayerState(Enum):
    IDLE = 0
    MOVING = 1

@dataclass
class Bullet(Sprite):
    w = 2
    h = 8
    speed = 3
    # uh why do i need to add these...
    keybindings = {}
    costumes = {}
    soundbank = {}

    def __init__(self, coord: SpriteCoordinate, color: int, cam: Camera):
        self.coord = coord
        self.color = color
        self.camera = cam
        self.is_dead = False
    
    def update(self):
        self.map_to_view(self.camera.y)

    def draw(self):
        pyxel.rect(self.coord.x, self.coord.y, self.w, self.h, self.color)


class Bullets():
    def __init__(self, camera: Camera):
        self.bullets: list[Bullet] = []
        self.camera = camera
    
    def append(self, bullet: Bullet):
        self.bullets.append(bullet)

    def draw(self):
        if len(self.bullets) > 0:
            for bullet in self.bullets:

                bullet.coord.y_map -= bullet.speed

                bullet.update()
                bullet.draw()
                if bullet.coord.y_map < 0:
                    bullet.is_dead = True

                if bullet.is_dead:
                    self.bullets.remove(bullet)
    
class Flame(Sprite):
    def __init__(self, cam: Camera):
        self.img = 0
        self.u = 32
        self.v = 16
        self.w = 16
        self.h = 8
        self.colkey = ALPHA_COL
        self.flames = [(32, 16), (32, 24)]
        self.coord = SpriteCoordinate(0, 0, 0, 0)
        self.ticker = Ticker(5)
        self.camera = cam
    
    def draw(self):
        if self.ticker.get():
            self.set_costume(self.flames[pyxel.frame_count % 2])

        pyxel.blt(self.coord.x, self.coord.y, self.img, self.u, self.v, self.w, self.h, self.colkey)

    def update(self):
        self.ticker.update()

    def flame_update(self, player_x: float, player_y: float, player_h: int):
        self.coord.x = player_x
        self.coord.y = player_y + player_h

@dataclass
class Player(Sprite):
    """
    Game player.
    Controls background stars, flame, and bullets.
    Stars are located in stars.py, while flame and bullets are combined in player.py (this file).
    """
    img = 0
    u = 32
    v = 0
    w = 16
    h = 16
    colkey = ALPHA_COL
    state = PlayerState.IDLE
    accel = 0.1
    drag = 0.04
    x_vel = 0
    y_vel = 0

    def __init__(self, game: GameStateManager):
        """
        Initialize player.
        Camera is needed to limit movement.
        """
        self.keybindings = {
            "player_right": KeyFunc(pyxel.KEY_RIGHT, lambda: self.move_handler(Direction.RIGHT)),
            "player_left": KeyFunc(pyxel.KEY_LEFT, lambda: self.move_handler(Direction.LEFT)),
            "player_up": KeyFunc(pyxel.KEY_UP, lambda: self.move_handler(Direction.UP)),
            "player_down": KeyFunc(pyxel.KEY_DOWN, lambda: self.move_handler(Direction.DOWN)),
            "player_shoot": KeyFunc(pyxel.KEY_SPACE, lambda: self.shoot(), KeyTypes.BTNP, hold_time=10, repeat_time=10),
        }

        self.soundbank = {
            "shoot": Sfx(SoundType.AUDIO, 0, 10),
            "explode": Sfx(SoundType.AUDIO, 0, 11),
        }

        self.costumes = {
            "ship_1": (32, 0),
            "ship_2": (48, 16),
            "ship_3": (32, 32),
        }

        self.statusbar_items = [
            StatusbarItem(self.get_speed, pyxel.COLOR_WHITE)
        ]
            
        level = game.levelhandler.get_curr()
        self.level_idx = level.idx
        self.levelmap = level.levelmap # only run ONCE; we don't want to get the level on every tick.
        self.bullet_color = level.bullet_color
        
        self.statusbar = game.statusbar
        self.statusbar.append(self.statusbar_items)
        self.coord = SpriteCoordinate(0, 0, tile_to_real(self.levelmap.level_width) // 2, tile_to_real(self.levelmap.level_height) - tile_to_real(4))
        self.init_costume(game.levelhandler.curr_level.ship)
        self.ticker = Ticker(3)
        self.camera = game.camera

        self.flame = Flame(self.camera)
        self.stars = Stars(100, game)
        self.bullets = Bullets(game.camera)

    def init_costume(self, ship: PlayerShip):
        match ship:
            case PlayerShip.SHIP1:
                self.set_costume(self.costumes["ship_1"])
            case PlayerShip.SHIP2:
                self.set_costume(self.costumes["ship_2"])
            case PlayerShip.SHIP3:
                self.set_costume(self.costumes["ship_3"])

    def move_handler(self, direction: Direction):
        match direction:
            case Direction.UP:
                self.y_vel -= self.accel
                self.coord.y_map -= self.accel
            case Direction.DOWN:
                self.y_vel += self.accel
                self.coord.y_map += self.accel
            case Direction.RIGHT:
                self.x_vel += self.accel
                self.coord.x_map += self.accel
            case Direction.LEFT:
                self.x_vel -= self.accel
                self.coord.x_map -= self.accel

    def move(self):
        self.coord.x_map += self.x_vel
        self.coord.y_map += self.y_vel
        self.x_vel -= self.drag * self.x_vel
        self.y_vel -= self.drag * self.y_vel

        if self.coord.x_map < self.speed:
            self.coord.x_map = self.speed
        elif self.coord.x_map > tile_to_real(self.levelmap.level_width) - self.w:
            self.coord.x_map = tile_to_real(self.levelmap.level_width) - self.w
        elif self.coord.y_map > tile_to_real(self.levelmap.level_height) - self.h:
            self.coord.y_map = tile_to_real(self.levelmap.level_height) - self.h
        elif self.coord.y_map < self.speed:
            self.coord.y_map = self.speed
        else:
            self.stars.update()

    def shoot(self):
        self.bullets.append(Bullet(
            SpriteCoordinate(0, 0, self.coord.x_map + self.w // 2 - Bullet.w, self.coord.y_map - self.h // 2),
            self.bullet_color,
            self.camera
            ))

    def cam_update(self):
        self.camera.y = self.coord.y_map

        if self.camera.y > tile_to_real(self.levelmap.level_height) - WINDOW_HEIGHT // 2:
            self.camera.y = tile_to_real(self.levelmap.level_height) - WINDOW_HEIGHT // 2
            self.camera.dir_y = 0
        elif self.camera.y < WINDOW_HEIGHT // 2:
            self.camera.y = WINDOW_HEIGHT // 2
            self.camera.dir_y = 0
        else:
            self.camera.dir_y = self.y_vel
            self.camera.dir_x = self.x_vel
        

    def update(self):
        self.cam_update()
        self.map_to_view(self.camera.y)
        self.flame.flame_update(self.coord.x, self.coord.y, self.h)

        if not self.level_idx == 3:
            self.flame.ticker.update()
            self.flame.update()
        

    def draw(self):
        self.stars.draw()
        self.flame.draw()
        self.move()

        self.bullets.draw()

        self.statusbar.draw()
        pyxel.blt(self.coord.x, self.coord.y, self.img, self.u, self.v, self.w, self.h, self.colkey)
    
    # Functions for statusbar
    def get_speed(self) -> str:
        magnitude = sqrt(self.y_vel * self.y_vel + self.x_vel * self.x_vel)
        magnitude = pyxel.floor(magnitude * 100)
        string = f"Speed: {magnitude} km/h"
        return string

