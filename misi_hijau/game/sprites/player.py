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

from dataclasses import dataclass
import pyxel
from enum import Enum
from math import sqrt # pyxel.sqrt(0) returns denormalized number; we need it to return 0.
from . import Sprite, SpriteCoordinate, bullets
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

    soundbank = {
        "shoot": Sfx(SoundType.AUDIO, 0, 10),
    }

    costumes = {
        "ship_1": (32, 0),
        "ship_2": (48, 16),
        "ship_3": (32, 32),
    }

    def __init__(self, game: GameStateManager, bullets: bullets.Bullets):
        self.keybindings = {
            "player_right": KeyFunc(pyxel.KEY_RIGHT, lambda: self.move_handler(Direction.RIGHT)),
            "player_left": KeyFunc(pyxel.KEY_LEFT, lambda: self.move_handler(Direction.LEFT)),
            "player_up": KeyFunc(pyxel.KEY_UP, lambda: self.move_handler(Direction.UP)),
            "player_down": KeyFunc(pyxel.KEY_DOWN, lambda: self.move_handler(Direction.DOWN)),
            "player_shoot": KeyFunc(pyxel.KEY_SPACE, lambda: self.shoot(), KeyTypes.BTNP, hold_time=10, repeat_time=10),
        }

        self.statusbar_items = [
            StatusbarItem(self.get_speed, pyxel.COLOR_WHITE)
        ]
            
        level = game.levelhandler.get_curr()
        self.level_idx = level.idx
        levelmap = level.levelmap # only run ONCE; we don't want to get the level on every tick.
        self.level_width = tile_to_real(levelmap.level_width)
        self.level_height = tile_to_real(levelmap.level_height)
        self.bullet_color = level.bullet_color
        
        self.statusbar = game.statusbar
        self.coord = SpriteCoordinate(0, 0, self.level_width // 2, self.level_height - tile_to_real(4))
        self.init_costume(game.levelhandler.curr_level.ship)
        self.ticker = Ticker(3)
        self.camera = game.camera
        self.soundplayer = game.soundplayer

        self.flame = Flame(self.camera)
        self.stars = Stars(100, game)
        self.bullets = bullets

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
        elif self.coord.x_map > self.level_width - self.w:
            self.coord.x_map = self.level_width - self.w
        else:
            self.stars.update()

        if self.coord.y_map > self.level_height - self.h:
            self.coord.y_map = self.level_height - self.h
        elif self.coord.y_map < self.speed:
            self.coord.y_map = self.speed
        else:
            self.stars.update()

    def shoot(self):
        self.soundplayer.play(self.soundbank["shoot"])
        self.bullets.append(self.coord.x_map + self.w // 2 - 2, self.coord.y_map - self.h // 2, self.bullet_color)

    def cam_update(self):
        self.camera.y = self.coord.y_map

        if self.camera.y > self.level_height - WINDOW_HEIGHT // 2:
            self.camera.y = self.level_height - WINDOW_HEIGHT // 2
            self.camera.dir_y = 0
        elif self.camera.y < WINDOW_HEIGHT // 2:
            self.camera.y = WINDOW_HEIGHT // 2
            self.camera.dir_y = 0
        else:
            self.camera.dir_y = self.y_vel
            self.camera.dir_x = self.x_vel
        

    def update(self):
        self.map_to_view(self.camera.y)
        self.cam_update()
        self.flame.flame_update(self.coord.x, self.coord.y, self.h)
        self.move()

        if not self.level_idx == 3:
            self.flame.ticker.update()
            self.flame.update()
        

    def draw(self):
        self.stars.draw()
        self.flame.draw()

        self.bullets.draw()

        pyxel.blt(self.coord.x, self.coord.y, self.img, self.u, self.v, self.w, self.h, self.colkey)
    
    # Functions for statusbar
    def test(self) -> str:
        string = f"{self.accel}"
        return string

    def get_speed(self) -> str:
        magnitude = sqrt(self.y_vel * self.y_vel + self.x_vel * self.x_vel)
        magnitude = pyxel.floor(magnitude * 100)
        string = f"Speed: {magnitude} km/h"
        return string

