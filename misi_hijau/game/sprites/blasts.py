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
from . import Sprite
from game.utils import Ticker
import game.events as events
from game.game_handler import GameComponents
from game.common import ALPHA_COL

class Blast(Sprite):
    w = 16
    h = 16

    costumes = {
        "blast_1": (16, 32),
        "blast_2": (0, 32),
        "blast_3": (0, 80)
    }

    def __init__(self, x: float, y: float):
        self.blast_stage: int = 1
        self.set_costume(self.costumes["blast_1"])
        self.coord.x = x
        self.coord.y = y
        self.ticker = Ticker(5)
    
    def update(self):
        self.ticker.update()
        if self.ticker.get():
            self.blast_stage += 1

    def draw(self):
        self.costume_change()
        pyxel.blt(self.coord.x, self.coord.y, 0, self.u, self.v, self.w, self.h, ALPHA_COL)
    
    def costume_change(self):
        self.set_costume(self.costumes["blast_2"]) if self.blast_stage == 3 else None
        self.set_costume(self.costumes["blast_3"]) if self.blast_stage == 4 else None

class BlastsHandler(Sprite):
    def __init__(self, game: GameComponents):
        self.game = game
        self.game.event_handler.add_handler(events.AppendBlastEffect.name, self.append_blast)
        self.blasts: list[Blast] = []
    
    def draw(self):
        for blast in self.blasts:
            blast.draw()

    def update(self):
        for blast in self.blasts:
            blast.update()
            if blast.blast_stage == 5:
                self.blasts.remove(blast)

    def append_blast(self, x: float, y: float, object_w: int, object_h: int):
        self.blasts.append(Blast(x - object_w // 2, y - object_h // 2))