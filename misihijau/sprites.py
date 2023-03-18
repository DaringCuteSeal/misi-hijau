# Copyright 2023 Cikitta Tjok

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Sprites for game

import pyxel
from utils import *
from enum import Enum

# Enums
class State(Enum):
    IDLE = 0
    MOVE = 1
    SHOOT = 2

# Actual sprites
@dataclass
class Player(Sprite):
    coord = Coordinate(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 8, 8)
    img = 0
    u = 16
    v = 24
    w = 8
    h = 8
    colkey = ALPHA_COL
    direction = Direction.DOWN
    speed = 2
    moving = False
    costume_i = 0
    state = State.IDLE
    ticker = Ticker(10)
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
    
    def __init__(self):
        """
        Initialize player.
        Camera is needed to limit movement.
        """
        self.keybindings = {
            "player_right": KeyFunc(pyxel.KEY_RIGHT, lambda: self.move(Direction.RIGHT)),
            "player_left": KeyFunc(pyxel.KEY_LEFT, lambda: self.move(Direction.LEFT)),
            "player_up": KeyFunc(pyxel.KEY_UP, lambda: self.move(Direction.UP)),
            "player_down": KeyFunc(pyxel.KEY_DOWN, lambda: self.move(Direction.DOWN))
        }

    def face(self, dir: Direction):
        """
        Switch character's direction and set the correct costume (circumventing the tick logic).
        """
        # If direction is already correct, don't switch costume.
        if dir == self.direction:
            return

        self.direction = dir

        match(dir):
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

    def move(self, dir: Direction):
        self.state = State.MOVE

        match(dir):
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
                if self.coord.y_map > self.speed:
                    self.coord.y_map -= self.speed
                if(
                    self.coord.y_map == self.speed
                    and self.coord.y < (WINDOW_HEIGHT // 2 + self.speed)
                    and self.coord.y > self.speed
                ):
                    self.coord.y -= self.speed

            case Direction.DOWN:
                self.face(Direction.DOWN)
                if self.coord.y_map < MAP_HEIGHT - self.speed:
                    self.coord.y_map += self.speed
                if(
                    self.coord.y_map == MAP_HEIGHT - self.speed
                    and self.coord.y > (WINDOW_HEIGHT // 2 - self.speed)
                    and self.coord.y < MAP_HEIGHT - self.speed
                ):
                    self.coord.y += self.speed

        # Since we only scroll vertically, the x_map is useless.
        # XXX Remove if need during refactoring.
        self.coord.x_map = self.coord.x
        self.update_anim()
        self.state = State.IDLE

    def update_anim(self):
        """
        Update costume (animation).
        """
        self.ticker.update()
        if not self.ticker.get():
            return

        match(self.direction):
            case Direction.RIGHT:
                self.w = 8
                if self.direction == Direction.LEFT:
                    self.coord.x += 8

                match(self.state):
                    case State.IDLE:
                        self.costume_toggle(self.costumes["r_1"], self.costumes["r_2"])
                    case State.SHOOT:
                        self.costume_toggle(self.costumes["shoot_r"], self.costumes["r_1"])
                    case State.MOVE:
                        self.costume_toggle(self.costumes["walk_r"], self.costumes["r_1"])

            case Direction.LEFT:
                self.w = -8
                if self.direction == Direction.RIGHT:
                    self.coord.x -= 8

                match(self.state):
                    case State.IDLE:
                        self.costume_toggle(self.costumes["r_1"], self.costumes["r_2"])
                    case State.SHOOT:
                        self.costume_toggle(self.costumes["shoot_r"], self.costumes["r_1"])
                    case State.MOVE:
                        self.costume_toggle(self.costumes["walk_r"], self.costumes["r_1"])
            
            case Direction.UP:
                self.w = 8
                match(self.state):
                    case State.IDLE:
                        self.costume_toggle(self.costumes["u_1"], self.costumes["u_2"])
                    case State.SHOOT:
                        self.costume_toggle(self.costumes["shoot_u"], self.costumes["u_1"])
                    case State.MOVE:
                        self.costume_toggle(self.costumes["walk_u"], self.costumes["u_1"])

            case Direction.DOWN:
                self.w = 8
                match(self.state):
                    case State.IDLE:
                        self.costume_toggle(self.costumes["f_1"], self.costumes["f_2"])
                    case State.SHOOT:
                        self.costume_toggle(self.costumes["shoot_f"], self.costumes["f_1"])
                    case State.MOVE:
                        self.costume_toggle(self.costumes["walk_f"], self.costumes["f_1"])

                
        self.set_costume(self.costume)
        self.costume_i = not self.costume_i