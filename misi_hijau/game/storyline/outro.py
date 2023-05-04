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

from core.sprite_classes import Sprite
from core.game_handler import GameHandler
from core.common import WINDOW_HEIGHT, WINDOW_WIDTH, KeyFunc
from res.resources_load import FINISH_SCREEN_IMAGE_PATH, TEMP_IMG_BANK_IDX
from game import events

class OutroPlane(Sprite):
    img = 0
    w = 16
    h = 16
    speed = 3

    costumes = {
        "1": (32, 32),
        "2": (48, 32)
    }

    def __init__(self, game_handler: GameHandler):
        self.game_handler = game_handler
        self.costume_idx = False
        self.costume_ticker = self.game_handler.game_components.ticker.attach(5)
        self._set_coord()
    
    def _set_coord(self):
        self.coord.y = WINDOW_HEIGHT + self.h
        self.coord.x = WINDOW_WIDTH // 2
    
    def update(self):
        if self.costume_ticker.get():
            self.costume_idx = not self.costume_idx
            self.set_costume(self.costumes["1"]) if self.costume_idx else self.set_costume(self.costumes["2"])

        self.coord.y -= self.speed

    def draw(self):
        pyxel.blt(self.coord.x, self.coord.y, self.img, self.u, self.v, self.w, self.h, self.colkey)

class OutroPlayer:
    QUIT_HINT_STRING = "q untuk keluar dari permainan..."

    def __init__(self, game_handler: GameHandler):
        self.game_handler = game_handler
        self.game_handler.game_components.event_handler.add_handler(events.FinishGame.name, self.show_outro)
    
    def show_outro(self):
        self.plane = OutroPlane(self.game_handler) # create plane for animation
        self.exit_game_keyfunc = KeyFunc([pyxel.KEY_Q, pyxel.KEY_ESCAPE], self.quit_game)
        self.game_handler.game_components.timer.attach(3).when_over(self.show_quit_hint)
        self.game_handler.callable_update = self.update
        self.game_handler.callable_draw = self.draw
        self.draw_background()
    
    def draw_background(self):
        pyxel.image(TEMP_IMG_BANK_IDX).load(0, 0, FINISH_SCREEN_IMAGE_PATH)
        pyxel.blt(0, 0, TEMP_IMG_BANK_IDX, 0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

    def show_quit_hint(self):
        quit_string_width = len(self.QUIT_HINT_STRING) * pyxel.FONT_WIDTH
        x = (WINDOW_WIDTH - quit_string_width) // 2
        y = WINDOW_HEIGHT - pyxel.FONT_HEIGHT - 10
        self.game_handler.game_components.event_handler.trigger_event(events.ShowBlinkingTextHint(x, y, self.QUIT_HINT_STRING, TEMP_IMG_BANK_IDX, True))

    def draw(self):
        self.draw_background()
        if self.plane:
            self.plane.draw()
        self.game_handler.game_components.game_ui.draw()
    
    def update(self):
        if self.plane:
            self.plane.update()
            if self.plane.coord.y + self.plane.h < 0:
                self.plane = None
    
    def quit_game(self):
        pyxel.quit()