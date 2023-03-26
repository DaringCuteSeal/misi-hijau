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

from . import Sprite, SpriteCoordinate
from ..components import Camera
import pyxel

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
        if self.is_sprite_in_viewport():
            pyxel.rect(self.coord.x, self.coord.y, self.w, self.h, self.color)

class Bullets(Sprite):
    def __init__(self, camera: Camera):
        self.bullets: list[Bullet] = []
        self.camera = camera
    
    def append(self, x: float, y: float, color: int):
        bullet = Bullet(SpriteCoordinate(-30, -30, x, y), color, self.camera)
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
  