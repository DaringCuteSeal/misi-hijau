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

### Sprites for game

from dataclasses import dataclass
import pyxel
from enum import Enum
from ..base import (
    ALPHA_COL,
    TILE_SIZE,
    WINDOW_HEIGHT,
    Coordinate,
    Direction,
    GameStateManager,
    KeyFunc,
    PlayerShip,
    Sfx,
    SoundType,
    SpriteObj,
    Ticker,
    tile_to_real 
)

class PlayerState(Enum):
    IDLE = 0
    MOVING = 1

class Flame(SpriteObj):
    def __init__(self):
        self.img = 0
        self.u = 32
        self.v = 16
        self.w = 16
        self.h = 8
        self.colkey = ALPHA_COL
        self.flames = [(32, 16), (32, 24)]
        self.coord = Coordinate(0, 0, 0, 0)
        self.ticker = Ticker(5)

@dataclass
class Player(SpriteObj):
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

    costumes = {
        "space1": (32, 0),
        "space2": (48, 16)
    }
    
    def __init__(self, game: GameStateManager, flame: Flame):
        """
        Initialize player.
        Camera is needed to limit movement.
        """
        self.keybindings = {
            "player_right": KeyFunc(pyxel.KEY_RIGHT, lambda: self.move_handler(Direction.RIGHT)),
            "player_left": KeyFunc(pyxel.KEY_LEFT, lambda: self.move_handler(Direction.LEFT)),
            "player_up": KeyFunc(pyxel.KEY_UP, lambda: self.move_handler(Direction.UP)),
            "player_down": KeyFunc(pyxel.KEY_DOWN, lambda: self.move_handler(Direction.DOWN)),
            "player_shoot": KeyFunc(pyxel.KEY_SPACE, lambda: self.shoot()),
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
            
        level = game.levelhandler.get_curr()
        self.level_idx = level.idx
        self.levelmap = level.levelmap # only run ONCE; we don't want to get the level on every tick.
        self.coord = Coordinate(0, 0, tile_to_real(self.levelmap.level_width) // 2, 450)
        self.init_costume(game.levelhandler.get_curr().ship)
        self.flame = flame
        self.camera = game.camera
        self.ticker = Ticker(3)

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
        if self.coord.x_map > tile_to_real(self.levelmap.level_width) - TILE_SIZE * 2:
            self.coord.x_map = tile_to_real(self.levelmap.level_width) - TILE_SIZE * 2
        if self.coord.y_map > tile_to_real(self.levelmap.level_height) - TILE_SIZE * 2:
            self.coord.y_map = tile_to_real(self.levelmap.level_height) - TILE_SIZE * 2
        if self.coord.y_map < self.speed:
            self.coord.y_map = self.speed

    def shoot(self):
        pass

    def flame_update(self):
        self.flame.coord.x = self.coord.x
        self.flame.coord.y = self.coord.y + self.h
        if self.flame.ticker.get():
            self.flame.set_costume(self.flame.flames[pyxel.frame_count % 2])
        self.flame.draw()

    def cam_update(self):
        self.camera.y = self.coord.y_map

        if self.camera.y > tile_to_real(self.levelmap.level_height) - WINDOW_HEIGHT // 2:
            self.camera.y = tile_to_real(self.levelmap.level_height) - WINDOW_HEIGHT // 2
        if self.camera.y < WINDOW_HEIGHT // 2:
            self.camera.y = WINDOW_HEIGHT // 2

    def draw(self):
        self.coord.y = self.coord.y_map - self.camera.y + WINDOW_HEIGHT / 2
        self.coord.x = self.coord.x_map
        self.move()
        self.cam_update()

        if not self.level_idx == 3:
            self.flame.ticker.update()
            self.flame_update()

        pyxel.blt(self.coord.x, self.coord.y, self.img, self.u, self.v, self.w, self.h, self.colkey)