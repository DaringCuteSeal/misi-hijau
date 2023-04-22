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
import os

from ..game_handler import GameComponents
from ..common import WINDOW_HEIGHT, KeyFunc, Sfx, SoundType
from res.story_slideshow_text import story_text
from .text_engine import TextEngine
from .. import events
from ..utils import Ticker

class StorylinePlayer:
    soundbank = {
        "music": Sfx(SoundType.MUSIC, 3, 0),
        "start_sfx": Sfx(SoundType.AUDIO, 0, 16),
        "typing": Sfx(SoundType.AUDIO, 1, 17),
    }
    string_collection = story_text

    SLIDESHOW_WAIT_STRING = "please press space to continue..."
    SLIDESHOW_WAIT_COORD = (WINDOW_HEIGHT - 10, 20)

    def __init__(self, game_components: GameComponents):
        self.game_components = game_components
        self.textengine = TextEngine(self.game_components)
        self.game_components.soundplayer.play(self.soundbank["music"], loop=True)
        self.game_components.event_handler.add_handler(events.SlideshowNext.name, self.slideshow_next_handler)
        self.blink_ticker = Ticker(5)
        self.slideshow_idx = 1

        self.set_keybindings()

    def set_keybindings(self):
        self.keybindings = {
            "slideshow_next": KeyFunc(pyxel.KEY_SPACE, self.slideshow_next_handler, active=True, hold_time=3, repeat_time=3)
        }

        self.game_components.keylistener.add(self.keybindings)
    
    #########
    # Intro #
    #########

    def slide_intro(self):
        pyxel.blt(0, 0, 1, 0, 0, 256, 256)
        self.game_components.timer.attach(4.8).when_over(self._show_slideshow_slide) # start slideshow after 5 seconds

    def _show_slideshow_slide(self):
        pyxel.image(1).load(0, 0, os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../../res/intro_slideshows/{self.slideshow_idx}.png"))

        self.game_components.soundplayer.play(self.soundbank["start_sfx"])
        self.game_components.soundplayer.play(self.soundbank["typing"])
        pyxel.cls(0)
        pyxel.blt(0, 0, 1, 256, 0, 256, 256)

        self.textengine.animate_text(self.string_collection["intro"][0], 5, 5, self._text_hint_wait, sfx=True, speed=0.02, color=pyxel.COLOR_WHITE)

    def _text_hint_wait(self):
        pyxel.text(self.SLIDESHOW_WAIT_COORD[0], self.SLIDESHOW_WAIT_COORD[1], self.SLIDESHOW_WAIT_STRING, pyxel.COLOR_WHITE)
        

    ##################
    # Key handlers #
    ##################
    def slideshow_next_handler(self):
        self._show_slideshow_slide
        self.slideshow_idx += 1