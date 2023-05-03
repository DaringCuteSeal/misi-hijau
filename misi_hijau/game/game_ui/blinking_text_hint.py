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

from core.game_handler import GameHandler
from core.utils import TickerItem
from core.game_ui_classes import UIComponent
from game import events

class BlinkingTextHint(UIComponent):
    """
    A blinking text to hint the player.
    """

    def __init__(self, game_handler: GameHandler):
        self.active = False
        self.coord.x = 0
        self.coord.y = 0
        self.game_handler = game_handler
        self.game_handler.game_components.event_handler.add_handler(events.ShowBlinkingTextHint.name, self.show)
        self.game_handler.game_components.event_handler.add_handler(events.HideBlinkingTextHint.name, self.hide)
        self.hint_text_blink_idx = 0
        
        # We instantiate a new ticker on every show() call. 
        # We use None | TickerItem so the draw() method won't crash the game if the ticker hasn't been properly initialized.
        self.hint_text_blink_ticker: None | TickerItem = None 

    def show(self, x: int, y: int, msg: str, background_img_idx: int):
        self.img = background_img_idx
        self.coord.x = x
        self.coord.y = y
        self.hint_text_blink_ticker = self.game_handler.game_components.ticker.attach(30)
        self.msg = msg
        self.msg_width = len(msg) * pyxel.FONT_WIDTH
        self.active = True
    
    def hide(self):
        self.active = False

    def _enable_text_hint(self):
        self.active = False

    def _draw(self):
        if self.hint_text_blink_ticker and self.hint_text_blink_ticker.get():
            self.hint_text_blink_idx = not self.hint_text_blink_idx

            if self.hint_text_blink_idx:
                pyxel.text(self.coord.x, self.coord.y, self.msg, pyxel.COLOR_WHITE)
            else: 
                # blit back of the text with the background image instead of constantly drawing everything (computationally cheaper)
                pyxel.blt(self.coord.x, self.coord.y, self.img, self.coord.x, self.coord.y, self.msg_width, pyxel.FONT_HEIGHT)

    def init_level(self):
        self.active = False

    def restart_level(self):
        self.active = False