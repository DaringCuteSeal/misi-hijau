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
from enum import Enum

# Enums
class PlayerState(Enum):
    IDLE = 0
    MOVE = 1
    SHOOT = 2

# Actual sprites
SoundBank = {
}

@dataclass
class Player(SpriteObj):
    coord = Coordinate(WINDOW_WIDTH // 2, 22, 128, 20)
    img = 0
    u = 16
    v = 24
    w = 8
    h = 8
    colkey = ALPHA_COL
    direction = Direction.DOWN
    speed = w
    moving = False
    costume_i = 0
    state = PlayerState.IDLE
    costumes = {
        # Left/right
        "r_1": (0, 16),
        "r_2": (8, 16),
        "shoot_r": (0, 24),
        "walk_r": (8, 24),

        # Up (back)
        "u_1": (16, 16),
        "u_2": (16, 16),
        "shoot_u": (32, 24),
        "walk_u": (24, 16),

        # Down (front)
        "f_1": (16, 24),
        "f_2": (16, 32),
        "shoot_f": (24, 32),
        "walk_f": (24, 24)
    }
    
    def __init__(self, game: GameStateManager):
        """
        Initialize player.
        Camera is needed to limit movement.
        """
        self.camera = game.camera
        self.ticker = game.ticker
        self.keybindings = {
            "player_right": KeyFunc(pyxel.KEY_RIGHT, lambda: self.move(Direction.RIGHT)),
            "player_left": KeyFunc(pyxel.KEY_LEFT, lambda: self.move(Direction.LEFT)),
            "player_up": KeyFunc(pyxel.KEY_UP, lambda: self.move(Direction.UP)),
            "player_down": KeyFunc(pyxel.KEY_DOWN, lambda: self.move(Direction.DOWN)),
            "player_shoot": KeyFunc(pyxel.KEY_SPACE, lambda: self.shoot())
        }

        self.soundbank: dict[str, Sfx] = {
            "shoot": Sfx(SoundType.AUDIO, 0, 10),
            "explode": Sfx(SoundType.AUDIO, 0, 11),
            "track": Sfx(SoundType.MUSIC, 0, 0)
        }
    def face(self, dir: Direction):
        """
        Switch character's direction and set the correct costume (circumventing the tick logic).
        """
        # If direction is already correct, don't switch costume.
        if dir == self.direction:
            return

        self.direction = dir

        match dir:
            case Direction.RIGHT:
                self.w = 8
                self.set_costume(self.costumes["r_1"])
            case Direction.LEFT:
                self.w = -8
                if self.direction == Direction.RIGHT:
                    self.coord.x -= 8
                self.set_costume(self.costumes["r_1"])
            case Direction.UP:
                self.w = 8
                self.set_costume(self.costumes["u_1"])
            case Direction.DOWN:
                self.w = 8
                self.set_costume(self.costumes["f_1"])

    def move_wait(self, dir: Direction):
        self.state = PlayerState.IDLE

    def move(self, dir: Direction):
        if not self.ticker.get(self.speed):
            return

        self.state = PlayerState.MOVE
        match dir:
            case Direction.RIGHT:
                self.face(Direction.RIGHT)
                if self.coord.x < WINDOW_WIDTH - tile_to_real(1) - self.speed:
                    self.coord.x += self.speed

            case Direction.LEFT:
                self.face(Direction.LEFT)
                if self.coord.x > self.speed:
                    self.coord.x -= self.speed

            case Direction.UP:
                self.face(Direction.UP)
                if self.coord.y_map > self.speed + 2:
                    self.coord.y_map -= self.speed

                if(
                    self.coord.y_map <= WINDOW_HEIGHT // 2 - self.speed
                    or self.coord.y_map >= MAP_HEIGHT - WINDOW_HEIGHT // 2 + self.speed
                    and self.coord.y_map > self.speed * 2
                ):
                    self.coord.y -= self.speed
                else:
                    self.camera.y -= self.camera.speed

                if self.coord.y_map <= WINDOW_HEIGHT // 2 - self.speed:
                    self.coord.y = self.coord.y_map

            case Direction.DOWN:
                self.face(Direction.DOWN)

                if self.coord.y_map < MAP_HEIGHT - self.speed - 2:
                    self.coord.y_map += self.speed

                if(
                    self.coord.y_map <= WINDOW_HEIGHT // 2 - self.speed
                    or self.coord.y_map >= MAP_HEIGHT - WINDOW_HEIGHT // 2 + self.speed
                    and self.coord.y_map > self.speed * 2
                ):
                    self.coord.y += self.speed
                else:
                    self.camera.y += self.camera.speed

                if self.coord.y_map >= MAP_HEIGHT - WINDOW_HEIGHT // 2 - self.speed:
                    self.coord.y = self.coord.y_map

       # Since we only scroll vertically, the x_map is useless.
        # XXX Remove if need during refactoring.
        self.coord.x_map = self.coord.x
        self.update_anim()
        self.state = PlayerState.IDLE

    def shoot(self):
        self.state = PlayerState.SHOOT

    def update_anim(self):
        """
        Update costume (animation).
        """
        # Only update animation when it's time to
        if not self.ticker.get(10):
            return

        match self.direction:
            case Direction.RIGHT:
                match self.state:
                    case PlayerState.IDLE:
                        self.costume_toggle(self.costumes["r_1"], self.costumes["r_2"])
                    case PlayerState.SHOOT:
                        self.costume_toggle(self.costumes["shoot_r"], self.costumes["r_1"])
                    case PlayerState.MOVE:
                        self.costume_toggle(self.costumes["walk_r"], self.costumes["r_1"])

            case Direction.LEFT:
                match self.state:
                    case PlayerState.IDLE:
                        self.costume_toggle(self.costumes["r_1"], self.costumes["r_2"])
                    case PlayerState.SHOOT:
                        self.costume_toggle(self.costumes["shoot_r"], self.costumes["r_1"])
                    case PlayerState.MOVE:
                        self.costume_toggle(self.costumes["walk_r"], self.costumes["r_1"])
            
            case Direction.UP:
                self.w = 8
                match self.state:
                    case PlayerState.IDLE:
                        self.costume_toggle(self.costumes["u_1"], self.costumes["u_2"])
                    case PlayerState.SHOOT:
                        self.costume_toggle(self.costumes["shoot_u"], self.costumes["u_1"])
                    case PlayerState.MOVE:
                        self.costume_toggle(self.costumes["walk_u"], self.costumes["u_1"])

            case Direction.DOWN:
                self.w = 8
                match self.state:
                    case PlayerState.IDLE:
                        self.costume_toggle(self.costumes["f_1"], self.costumes["f_2"])
                    case PlayerState.SHOOT:
                        self.costume_toggle(self.costumes["shoot_f"], self.costumes["f_1"])
                    case PlayerState.MOVE:
                        self.costume_toggle(self.costumes["walk_f"], self.costumes["f_1"])

                
        self.set_costume(self.costume)
        self.costume_i = not self.costume_i