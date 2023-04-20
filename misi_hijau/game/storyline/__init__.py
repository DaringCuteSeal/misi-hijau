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
from ..common import Sfx, SoundType
from res.story_slideshow_text import story_text
from .text_engine import TextEngine
from .. import events

class StorylinePlayer:
    soundbank = {
        "music": Sfx(SoundType.MUSIC, 3, 0),
        "start_sfx": Sfx(SoundType.AUDIO, 0, 16),
        "typing": Sfx(SoundType.AUDIO, 1, 17),
    }
    string_collection = story_text

    def __init__(self, game_components: GameComponents):
        self.game_components = game_components
        self.textengine = TextEngine(self.game_components)
        self.game_components.soundplayer.play(self.soundbank["music"], loop=True)
    
    def slide_intro(self):
        pyxel.blt(0, 0, 1, 0, 0, 256, 256)
        self.game_components.timer.attach(4.8).when_over(self._start_intro_text_story) # start slideshow after 5 seconds

    def _start_intro_text_story(self):
        pyxel.image(1).load(0, 0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../res/intro_slideshows/1.png"))

        self.game_components.soundplayer.play(self.soundbank["start_sfx"])
        self.game_components.soundplayer.play(self.soundbank["typing"])
        pyxel.cls(0)
        pyxel.blt(0, 0, 1, 256, 0, 256, 256)

        self.textengine.animate_text(self.string_collection["intro"][0], 5, 5, sfx=True, speed=0.02, color=pyxel.COLOR_WHITE)
        # self.game_components.event_handler.trigger_event(events.StartGame)