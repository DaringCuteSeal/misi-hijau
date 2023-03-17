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

# Actual sprites
@dataclass
class Player(Sprite):
    coord = Coordinate(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 )
    img = 0
    u = 0
    v = 16
    w = 8
    h = 8
    colkey = ALPHA_COL
    direction = Direction.RIGHT
    speed = 2
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
        self.direction = dir

    def move(self, dir: Direction):
        match(dir):
            case Direction.RIGHT:
                self.coord.x += self.speed
            case Direction.LEFT:
                self.coord.x -= self.speed
            case Direction.UP:
                if self.coord.y_map > self.speed:
                    self.coord.y -= self.speed
                    self.coord.y_map -= self.speed

            case Direction.DOWN:
                if self.coord.y_map < MAP_HEIGHT - self.speed:
                    self.coord.y += self.speed
                    self.coord.y_map += self.speed

        # Since we only scroll vertically, the x_map is useless.
        # XXX Remove if need during refactoring.
        self.coord.x_map = self.coord.x