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

from typing import Callable, Optional
import pyxel
from core.game_handler import GameHandler
from core.common import WINDOW_WIDTH, Sfx, SoundType
from core.game_ui_classes import UIComponent
from .. import events

class TextEngine(UIComponent):
    typing_sfx = Sfx(SoundType.AUDIO, 1, 17)
    TIMER_ID = "text_engine"

    def __init__(self, game_handler: GameHandler):
        self.active = False
        self.game_handler = game_handler
        self.timer = self.game_handler.game_components.timer
        self.soundplayer = self.game_handler.game_components.soundplayer
        self._is_interrupted: bool = False
        self.strings_collection: dict[str, list[str]] = {}
        self.current_string: str = ''
        self.current_color: int = pyxel.COLOR_WHITE
        self.current_speed: float = 0.03
        self.string_pos: int = 0
        self.use_sfx: bool = False
        self.function_when_done: Optional[Callable[..., None]] = None
        self._init_event_handlers()

    def _init_event_handlers(self):
        self.game_handler.game_components.event_handler.add_handler(events.TextengineInterrupt.name, self._interrupt_handler)
        self.game_handler.game_components.event_handler.add_handler(events.TextEngineAnimateText.name, self.animate_text)

    def _wrap_string(self, string: str) -> str:
        """
        Generate a wrapped string that doesn't overflow beyond the screen size.
        """
        words: list[str] = string.split()
        lines: list[str] = []
        current_line: str = ''
        for word in words:
            if (len(current_line + word) + 1) * pyxel.FONT_WIDTH + self.x > WINDOW_WIDTH:
                lines.append(current_line.strip())
                current_line = ''
            current_line += word + ' '
        if current_line:
            lines.append(current_line.strip())
        return '\n'.join(lines)
    
    def animate_text(self,
                     string: str,
                     x: int,
                     y: int,
                     function_when_done: Optional[Callable[..., None]] = None,
                     sfx: bool = False,
                     speed: float = 0.03,
                     color: int = pyxel.COLOR_WHITE):
        """
        Animate a string (with typing effect).
        """
        self.active = True
        self._interrupt_reset()

        self.string_pos = 0
        self.x = x
        self.y = y
        self.current_string = self._wrap_string(string)
        self.current_color = color
        self.current_speed = speed
        self.use_sfx = sfx
        self.function_when_done = function_when_done

        if self.use_sfx:
            self.soundplayer.play(self.typing_sfx, loop=True)
        self._recursively_increment_length()
    
    def _recursively_increment_length(self):
        if self._is_interrupted:
            self._interrupt_reset()
            return

        if self.string_pos != len(self.current_string):
            self.timer.attach(self.current_speed, self.TIMER_ID).when_over(self._recursively_increment_length)
            self.string_pos += 1
            # self._draw() # only draw when needed. Not clearing the text from before is fine, because the current string is just the previous string plus a new character.
        else:
            if self.use_sfx:
                self.soundplayer.stop_sfx_channel_playback(self.typing_sfx)
            self.function_when_done() if self.function_when_done else None
                
    def clear_text(self):
        self.string_pos = 0
    
    def _draw(self):
        pyxel.text(self.x, self.y, self.current_string[:self.string_pos], self.current_color)
    
    def _interrupt_handler(self):
        self.soundplayer.stop_sfx_channel_playback(self.typing_sfx)
        self.active = False
        self._is_interrupted = True
    
    def _interrupt_reset(self):
        self.soundplayer.stop_sfx_channel_playback(self.typing_sfx)
        self._is_interrupted = False
        self.timer.destroy_by_id(self.TIMER_ID)
    
    def init_level(self):
        pass

    def restart_level(self):
        pass