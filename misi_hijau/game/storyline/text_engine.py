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

# from pyxelunicode import PyxelUnicode # type: ignore # there's no stub file for this package.
from typing import Callable, Optional
import pyxel
from ..game_handler import GameComponents
from ..common import WINDOW_WIDTH, Sfx, SoundType

class TextEngine():
    typing_sfx = Sfx(SoundType.AUDIO, 1, 17)

    def __init__(self, game_components: GameComponents):
        # self.pyuni = PyxelUnicode(FONT_PATH, 12, 1)
        self.timer = game_components.timer
        self.soundplayer = game_components.soundplayer
        self.strings_collection: dict[str, list[str]] = {}
        self.current_string: str = ''
        self.current_color: int = pyxel.COLOR_WHITE
        self.current_speed: float = 0.03
        self.string_pos: int = 0
        self.use_sfx: bool = False
        self.function_when_done: Optional[Callable[..., None]] = None
    
    def _wrap_string(self, string: str) -> str:
        words = string.split()
        lines: list[str] = []
        current_line = ''
        for word in words:
            if (len(current_line + word) + 1) * pyxel.FONT_WIDTH + self.x > WINDOW_WIDTH:
                lines.append(current_line.strip())
                current_line = ''
            current_line += word + ' '
        if current_line:
            lines.append(current_line.strip())
        return '\n'.join(lines)
    
    def animate_text(self, string: str, x: int, y: int, function_when_done: Optional[Callable[..., None]] = None, sfx: bool = False, speed: float = 0.03, color: int = pyxel.COLOR_WHITE):
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
        if self.string_pos != len(self.current_string):
            self.timer.attach(self.current_speed).when_over(self._recursively_increment_length)
            self.string_pos += 1
            self._draw() # only draw when needed. Not clearing the text from before is fine, because the current string is just the previous string plus a new character.
        else:
            if self.use_sfx:
                self.soundplayer.stop_sfx_channel_playback(self.typing_sfx)
            self.function_when_done() if self.function_when_done else None
                
    def clear_text(self):
        self.string_pos = 0
    
    def _draw(self):
        # self.pyuni.text(self.x, self.y, self.current_string[:self.string_pos], self.current_color) # type: ignore # the author of PyxelUnicode didn't specify the type for the `s` parameter :)
        pyxel.text(self.x, self.y, self.current_string[:self.string_pos], self.current_color)