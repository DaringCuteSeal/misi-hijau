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

import pyxel
from ..base import *

# Actual sprites
SoundBank = {
}

@dataclass
class Player(SpriteObj):
    img = 0
    u = 32
    v = 0
    w = 16
    h = 16
    colkey = ALPHA_COL
    direction = Direction.DOWN
    speed = 3
    moving = False
    costume_i = 0
    coord = Coordinate(0, 0, 3, 450)
    costumes = {
    }
    
    def __init__(self, game: GameStateManager):
        """
        Initialize player.
        Camera is needed to limit movement.
        """
        self.camera = game.camera
        self.level = game.levelhandler.get_curr().idx
        self.ticker = game.ticker
        self.keybindings = {
            "player_right": KeyFunc(pyxel.KEY_RIGHT, lambda: self.move(Direction.RIGHT)),
            "player_left": KeyFunc(pyxel.KEY_LEFT, lambda: self.move(Direction.LEFT)),
            "player_up": KeyFunc(pyxel.KEY_UP, lambda: self.move(Direction.UP)),
            "player_down": KeyFunc(pyxel.KEY_DOWN, lambda: self.move(Direction.DOWN)),
            "player_shoot": KeyFunc(pyxel.KEY_SPACE, lambda: self.shoot())
        }

        self.soundbank = {
            "shoot": Sfx(SoundType.AUDIO, 0, 10),
            "explode": Sfx(SoundType.AUDIO, 0, 11),
            "track": Sfx(SoundType.MUSIC, 0, 0)
        }

        self.costumes = {
            "ship_1": (32, 0),
            "ship_2": (48, 16),
            "ship_3": (32, 32),
        }

    def move(self, direction: Direction):
        match direction:
            case Direction.RIGHT:
                if self.coord.x_map < tile_to_real(MAP_WIDTH) - self.speed - TILE_SIZE*2:
                    self.coord.x_map += self.speed

            case Direction.LEFT:
                if self.coord.x_map > self.speed:
                    self.coord.x_map -= self.speed

            case Direction.UP:
                if self.coord.y_map > self.speed:
                    self.coord.y_map -= self.speed

            case Direction.DOWN:
                if self.coord.y_map < tile_to_real(MAP_HEIGHT) - self.speed - TILE_SIZE*2:
                    self.coord.y_map += self.speed
    
    def cam_update(self):
        self.camera.y = self.coord.y_map

        if self.camera.y > tile_to_real(MAP_HEIGHT) - WINDOW_HEIGHT // 2:
            self.camera.y = tile_to_real(MAP_HEIGHT) - WINDOW_HEIGHT // 2
        if self.camera.y < WINDOW_HEIGHT // 2:
            self.camera.y = WINDOW_HEIGHT // 2

    def costume_update():
        self.set_costume(self.c)

    def draw(self):

        self.coord.y = self.coord.y_map - self.camera.y + WINDOW_HEIGHT // 2
        self.coord.x = self.coord.x_map
        self.cam_update()
        self.costume_update()

        pyxel.blt(self.coord.x, self.coord.y, self.img, self.u, self.v, self.w, self.h, self.colkey)