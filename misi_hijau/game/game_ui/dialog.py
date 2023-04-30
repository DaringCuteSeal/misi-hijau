# Copyright 2023 Cikitta Tjok <daringcuteseal@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pyxel

from typing import Optional, Callable, Any

from ..common import KeyFunc, WINDOW_WIDTH, WINDOW_HEIGHT, Sfx, SoundType
from ..game_handler import GameHandler
from .game_ui_classes import UIComponent, UIComponentCoordinate
from .. import events

class Dialog(UIComponent):
    soundbank = {
        "popup": Sfx(SoundType.AUDIO, 0, 16),
    }

    def __init__(self, game_handler: GameHandler):
        self.timer = game_handler.game_components.timer
        self.soundplayer = game_handler.game_components.soundplayer
        self.tmp_keyfunc = KeyFunc([pyxel.KEY_SPACE], self.hide, active=False)
        self._alter_keyfunc_state(False)
        self.function_when_done: Optional[Callable[..., Any]] = None
        self.text_gap: int = 5
        self.w: int = 0
        self.message: str = ''
        self.bg_color: int = pyxel.COLOR_WHITE
        self.message_width: int = 0
        self.text_color: int = pyxel.COLOR_BLACK

        game_handler.game_components.keylistener.add({"dialog_dismiss_btn": self.tmp_keyfunc})
        game_handler.game_components.event_handler.add_handler(events.ShowDialog.name, self.show)

        self.coord = UIComponentCoordinate(0, 0)
    
    def show(self,
            message: str,
            width: int,
            text_color: int,
            bg_color: int,
            text_gap: int = 5,
            function_when_done: Optional[Callable[..., Any]] = None,
            key_dismiss: int = pyxel.KEY_SPACE,
            sfx: bool = False, 
            show_dismiss_msg: bool = True) -> None:
        
        self.tmp_keyfunc.binding = [key_dismiss]
        self.function_when_done = function_when_done
        self.text_gap = text_gap
        self._calculate_dialog_size(width, message)
        self.bg_color = bg_color
        self.text_color = text_color
        self._calculate_dialog_pos()

        self.timer.attach(1).when_over(lambda: self._alter_keyfunc_state(True))

        if sfx:
            self.soundplayer.play(self.soundbank["popup"])

        self.active = True

    def _calculate_dialog_size(self, w: int, message: str):
        self.w = w + self.text_gap * 2
        self.message = self._wrap_string(message)

        self.message_rows_count = len(self.message.splitlines())
        self.message_width = max([len(length) for length in self.message.splitlines()])

        self.h = (self.message_rows_count * pyxel.FONT_HEIGHT) + self.text_gap * 2

    def hide(self):
        self.tmp_keyfunc.active = False
        self.active = False

    def _calculate_dialog_pos(self):
        self.coord.x = (WINDOW_WIDTH - self.w - 2 * self.text_gap) // 2
        self.coord.y = (WINDOW_HEIGHT - self.h - 2 * self.text_gap) // 2

    def _draw(self):
        pyxel.rect(self.coord.x, self.coord.y, self.w, self.h, self.bg_color)
        self._draw_text()
    
    def _alter_keyfunc_state(self, state: bool):
        self.tmp_keyfunc.active = state

    def _draw_text(self):
        pyxel.text(self.coord.x + (self.w - (self.message_width * pyxel.FONT_WIDTH))/2, self.coord.y + self.text_gap, self.message, self.text_color)
        
    def _wrap_string(self, string: str) -> str:
        """
        Generate a wrapped string that doesn't overflow beyond the dialog size.
        """

        words: list[str] = string.split()
        lines: list[str] = []
        current_line: str = ''

        for word in words:
            if (len(current_line + word) + 1) * pyxel.FONT_WIDTH + self.coord.x + self.text_gap * 2 > self.w:
                lines.append(current_line.strip())
                current_line = ''
            current_line += word + ' '
        
        if current_line:
            lines.append(current_line.strip())

        return '\n'.join(lines)
    
    def init_level(self):
        pass

    def restart_level(self):
        pass