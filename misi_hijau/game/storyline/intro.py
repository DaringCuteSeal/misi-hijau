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

from res.storyline_text import story_text

from ..game_handler import GameHandler
from res.resources_load import INTRO_SLIDESHOW_IMAGE_PATH, SPLASH_SCREEN_IMAGE, INSTRUCTIONS_IMAGE_PATH
from ..common import WINDOW_HEIGHT, KeyFunc, Sfx, SoundType
from .components.text_engine import TextEngine
from .. import events

class StorylinePlayer:
    soundbank = {
        "music": Sfx(SoundType.MUSIC, 3, 0),
        "start_sfx": Sfx(SoundType.AUDIO, 0, 16),
        "instruction_sfx": Sfx(SoundType.AUDIO, 0, 18)
    }
    string_collection = story_text

    TEXTENGINE_BORDER = 5

    SLIDESHOW_WAIT_STRING = "tekan spasi untuk lanjut..."
    SLIDESHOW_WAIT_COORD = (5, WINDOW_HEIGHT - pyxel.FONT_HEIGHT - 5)
    SLIDESHOW_WAIT_BORDER_WIDTH = len(SLIDESHOW_WAIT_STRING) * pyxel.FONT_WIDTH
    SLIDESHOW_WAIT_BORDER_HEIGHT = pyxel.FONT_HEIGHT

    INTRO_SLIDESHOW_COUNT = 6

    def __init__(self, game_handler: GameHandler):
        self.game_handler = game_handler
        game_components = self.game_handler.game_components

        self.textengine = TextEngine(game_components)

        game_components.soundplayer.play(self.soundbank["music"], loop=True)
        game_components.event_handler.add_handler(events.SlideshowNext.name, self.slideshow_next_handler)

        self.hint_text_blink_ticker = game_components.ticker.attach(30)
        self.hint_text_blink_idx = False

        self.slideshow_idx = 1

        self.set_keybindings()


    def set_keybindings(self):
        self.keybindings = {
            "slideshow_next": KeyFunc([pyxel.KEY_SPACE], lambda: self.game_handler.game_components.event_handler.trigger_event(events.SlideshowNext), active=False, repeat_time=3)
        }

        self.game_handler.game_components.keylistener.add(self.keybindings)
    
    ##################
    # Main functions #
    ##################

    def slide_intro(self):
        pyxel.image(1).load(0, 0, SPLASH_SCREEN_IMAGE)
        pyxel.blt(0, 0, 1, 0, 0, 256, 256)
        self.game_handler.game_components.timer.attach(4.8).when_over(self._show_slideshow_slide) # start slideshow after 5 seconds
        
    def _show_slideshow_slide(self):
        self._post_slideshow_show()

        self._load_slide_background_image(self.slideshow_idx)
        self._draw_background()
        self._play_slide_sfx()

        self.textengine.animate_text(self.string_collection["intro"][self.slideshow_idx - 1], self.TEXTENGINE_BORDER, self.TEXTENGINE_BORDER, lambda: self.game_handler.game_components.timer.attach(1).when_over(self._enable_spacebar_hint), sfx=True, speed=0.02, color=pyxel.COLOR_WHITE)

    def _enable_spacebar_hint(self):
        self.game_handler.callable_draw = self._text_hint_wait # activate the text hint loop

    def _text_hint_wait(self):
        if self.hint_text_blink_ticker.get():
            self.hint_text_blink_idx = not self.hint_text_blink_idx

            if self.hint_text_blink_idx:
                pyxel.text(self.SLIDESHOW_WAIT_COORD[0], self.SLIDESHOW_WAIT_COORD[1], self.SLIDESHOW_WAIT_STRING, pyxel.COLOR_WHITE)
            else: 
                # blit back of the text with the background image instead of constantly drawing everything (computationally cheaper)
                pyxel.blt(self.SLIDESHOW_WAIT_COORD[0], self.SLIDESHOW_WAIT_COORD[1], 1, self.SLIDESHOW_WAIT_COORD[0], self.SLIDESHOW_WAIT_COORD[1], self.SLIDESHOW_WAIT_BORDER_WIDTH, self.SLIDESHOW_WAIT_BORDER_HEIGHT)

    def _play_slide_sfx(self):
        self.game_handler.game_components.soundplayer.play(self.soundbank["start_sfx"])
    
    def _load_slide_background_image(self, idx: int):
        pyxel.image(1).load(0, 0, os.path.join(INTRO_SLIDESHOW_IMAGE_PATH, f"{idx}.png"))
    
    def _draw_background(self):
        pyxel.blt(0, 0, 1, 0, 0, 256, 256) # draw background image

    def _post_slideshow_show(self):
        """
        Functions to be run after showing a slideshow.
        """
        self.game_handler.game_components.event_handler.trigger_event(events.TextengineInterrupt)
        self._alter_keylistener_state(False)
        self.game_handler.callable_draw = None
        self.game_handler.game_components.timer.attach(0.2).when_over(lambda: self._alter_keylistener_state(True))

    ################
    # Instructions #
    ################

    def show_instructions(self):
        self._post_slideshow_show()
        pyxel.image(1).load(0, 0, INSTRUCTIONS_IMAGE_PATH)
        self.game_handler.game_components.soundplayer.play(self.soundbank["instruction_sfx"])
        pyxel.blt(0, 0, 1, 0, 0, 256, 256)

    ################
    # Key handlers #
    ################

    def _alter_keylistener_state(self, state: bool):
        self.keybindings["slideshow_next"].active = state

    def slideshow_next_handler(self):
        if self.slideshow_idx < self.INTRO_SLIDESHOW_COUNT: # a normal slideshow
            self.slideshow_idx += 1
            self._show_slideshow_slide()
        elif self.slideshow_idx == self.INTRO_SLIDESHOW_COUNT: # show instructions on last slideshow
            self.slideshow_idx += 1
            self.show_instructions()
        else:
            self.game_handler.game_components.event_handler.trigger_event(events.StartGame)
            self._alter_keylistener_state(False)