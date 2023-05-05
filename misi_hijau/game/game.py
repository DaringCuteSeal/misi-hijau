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

"""
Game loop handler.
"""

import pyxel

from . import events

from core.common import KeyFunc, KeyType

from core import components
from core.game_handler import GameComponents, GameHandler

from res.sprites import SpritesFactory
from res.ui import UIComponentFactory
from res.levels import levels, LEVELS_COUNT

from game.storyline.intro import IntroPlayer
from game.storyline.outro import OutroPlayer
from game.storyline.story_dialogs import InGameStoryline

class Game():
    ##################
    # Initialization #
    ##################

    def __init__(self):
        """
        Game initialization.
        """
        game_components = self.init_game_components()

        self.init_game_handler(game_components) # set up game handler

        self._init_event_handlers() # add event handlers
        self.ui_stars = None # stars are separated from the other UI components so it can be drawn first
        self.init_ui() # initialize UI components directly
        self._start_intro_slideshow() # start intro
        self._init_story_dialog() # instantiate ingame storyline
        
        # debugging
        self.attach_debug_key()

    def _start_intro_slideshow(self):
        self.game_handler.callable_draw = self.ui_only_draw
        self.intro_player = IntroPlayer(self.game_handler)
        self.intro_player.slide_intro()
    
    def _start_outro_slide(self):
        self.outro_player = OutroPlayer(self.game_handler)
    
    def _init_story_dialog(self):
        self.story_dialog = InGameStoryline(self.game_handler)

    def _init_event_handlers(self):
        self.game_handler.game_components.event_handler.add_handler(events.UpdateStatusbar.name, self.update_statusbar)
        self.game_handler.game_components.event_handler.add_handler(events.LevelRestart.name, self.level_restart)
        self.game_handler.game_components.event_handler.add_handler(events.LevelNext.name, self.increment_level)
        self.game_handler.game_components.event_handler.add_handler(events.StartGame.name, self.start_game)
        self.game_handler.game_components.event_handler.add_handler(events.StopGameLoop.name, self.stop_game_loop)
        self.game_handler.game_components.event_handler.add_handler(events.ResumeGameLoop.name, self.resume_game_loop)

    def init_game_components(self):
        """
        Set up (create) game components.
        """
        camera = components.Camera()
        soundplayer = components.SoundPlayer()
        keylistener = components.KeyListener()
        statusbar = components.GameStatusbar()
        game_sprites = components.GameSprites()
        event_handler = components.EventHandler()
        ui_handler = components.GameUI()
        ticker = components.TickerHandler()
        timer = components.Timer()
        game_components = GameComponents(soundplayer, camera, keylistener, statusbar, game_sprites, ui_handler, event_handler, ticker, timer)
        return game_components
        
    def init_game_handler(self, game_components: GameComponents):
        """
        Set up the main game handler.
        """
        level_handler = components.LevelHandler(levels)
        self.game_handler = GameHandler(level_handler, game_components)
        self.game_handler.levelhandler.set_lvl_by_idx(1)
   
    #########
    # Loops #
    #########

    def game_loop_update(self):
        """
        Game scene update loop.
        """
        self.game_handler.game_components.game_sprites.update()
    
    def ui_only_draw(self):
        """
        UI components-only draw loop.
        """
        self.game_handler.game_components.game_ui.draw()

    def game_loop_draw(self):
        """
        Game scene draw loop.
        """
        # Draw the black background to prevent ghosting effect
        pyxel.cls(pyxel.COLOR_BLACK)

        # Draw the stars.
        self.ui_stars.draw() if self.ui_stars else None

        # Draw all the game stuff on top of the black background
        self.game_handler.game_components.camera.draw(self.game_handler.levelhandler.curr_level.levelmap)

        # Sprites
        self.game_handler.game_components.game_sprites.draw()

        # Game UI components
        self.game_handler.game_components.game_ui.draw()

        # Statusbar
        self.game_handler.game_components.statusbar.draw()
    
    #####################
    # Enitity creations #
    #####################

    def init_sprites(self):
        self.sprites_factory = SpritesFactory(self.game_handler)
        sprites_handler = self.game_handler.game_components.game_sprites
        sprites_handler.append_sprites_handler(self.sprites_factory.create_sprite_handlers())
        sprites_handler.append_tilemap_sprites(self.sprites_factory.create_tilemap_sprites())
        sprites_handler.append_raw_sprites(self.sprites_factory.create_raw_sprites())
        self.assign_keybindings_to_sprites()
        self.append_sprites_statusbar()
        self.game_handler.game_components.statusbar.update()

    def assign_keybindings_to_sprites(self):
        keybinds = self.game_handler.game_components.game_sprites.get_keybinds()
        self.game_handler.game_components.keylistener.append(keybinds)

    def append_sprites_statusbar(self):
        statusbar_items = self.game_handler.game_components.game_sprites.get_statusbars()
        self.game_handler.game_components.statusbar.append(statusbar_items)

    def init_ui(self):
        self.ui_factory = UIComponentFactory(self.game_handler)
        game_ui_handler = self.game_handler.game_components.game_ui
        game_ui_handler.append(self.ui_factory.create_ui_components())
        self.ui_stars = self.ui_factory.create_stars()

    ##################
    # Event handlers #
    ##################

    def update_statusbar(self):
        self.game_handler.game_components.statusbar.update()
    
    def level_restart(self):
        self.game_handler.callable_draw = self.game_loop_draw

        self.game_handler.game_components.game_sprites.restart_level()
        self.game_handler.game_components.game_ui.restart_level()
        self.game_handler.game_components.statusbar.update() # make sure the new item values show up

    def setup_next_level(self):
        self.game_handler.set_callable_draw(self.game_loop_draw)
        self.game_handler.game_components.game_sprites.init_level()
        self.game_handler.game_components.game_ui.init_level()
        self.game_handler.game_components.statusbar.update() # make sure the new item values show up
    
    def increment_level(self):
        curr_level = self.game_handler.levelhandler.get_curr_lvl_idx()

        if curr_level == LEVELS_COUNT:
            self._start_outro_slide()
            self.game_handler.game_components.event_handler.trigger_event(events.FinishGame)
            self.game_handler.game_components.event_handler.remove_handler(events.LevelNext.name, self.increment_level) # level should not incremenet anymore
            return

        self.game_handler.game_components.event_handler.trigger_event(events.ResumeGameLoop)
        self.game_handler.levelhandler.set_lvl_by_idx(curr_level + 1)
        self.game_handler.game_components.event_handler.trigger_event(events.ShowLevelDialog) # show dialog at start
        self.setup_next_level()

    def start_game(self):
        self.init_sprites()
        self.game_handler.callable_draw = self.game_loop_draw
        self.game_handler.callable_update = self.game_loop_update
    
    def resume_game_loop(self):
        self.game_handler.set_callable_draw(self.game_loop_draw)
        self.game_handler.set_callable_update(self.game_loop_update)
    
    def stop_game_loop(self):
        self.game_handler.set_callable_draw(self.ui_only_draw)
        self.game_handler.set_callable_update(None)

    #############################
    # Draw and update functions #
    #############################

    def draw(self):
        """
        Call the game_handler.callable_draw method.
        """
        self.game_handler.draw()

    def update(self):
        """
        Call the game_handler.callable_update method.
        """
        self.game_handler.update()

    #############
    # Debugging #
    #############
 
    def attach_debug_key(self):
        self.game_handler.game_components.keylistener.add("debug_key", KeyFunc([pyxel.KEY_BACKSPACE],self._debug_show_level_stats, KeyType.BTNP, hold_time=10, repeat_time=100))
    
    def _debug_show_level_stats(self):
        self.game_handler.game_components.event_handler.trigger_event(events.LevelNext)