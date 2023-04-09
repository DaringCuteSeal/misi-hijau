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

from game.common import WINDOW_HEIGHT, WINDOW_WIDTH

from game import events

from game import components
from game.game_handler import GameComponents, GameHandler

from res.sprites import SpritesFactory
from res.ui import UIComponentFactory
from res.levels import levels

class Game():
    def __init__(self):
        """
        Game initialization.
        """
        # Set up components
        # Make sure the keybind_setup is on the LAST list
        camera = components.Camera()
        soundplayer = components.SoundPlayer()
        keylistener = components.KeyListener()
        statusbar = components.GameStatusbar()
        game_sprites = components.GameSprites()
        event_handler = components.EventHandler()
        ui_handler = components.GameUI()
        game_components = GameComponents(soundplayer, camera, keylistener, statusbar, game_sprites, ui_handler, event_handler)

        # Set up the main game handler
        level_handler = components.LevelHandler(levels)
        self.game_handler = GameHandler(level_handler, game_components)
        self.game_handler.levelhandler.set_lvl_by_idx(1)

        # Set up sprites
        self.init_sprites()
        self.init_ui()

        # Add event handler
        self.game_handler.game_components.event_handler.add_handler(events.UpdateStatusbar.name, self.update_statusbar)
        self.game_handler.game_components.event_handler.add_handler(events.LevelRestart.name, self.level_restart)
        self.game_handler.game_components.event_handler.add_handler(events.LevelNext.name, self.level_next)

        # Debugging
        # self.debugger = Debugger(self.spr_player, self.game_handler.game_components)
        
    def update(self):
        """
        Update game state.
        """
        self.game_handler.game_components.game_sprites.update()
        self.game_handler.game_components.keylistener.check()
    
    def draw_game_loop(self):
        """
        Draw game scene.
        """
        # Draw the black background to prevent ghosting effect
        pyxel.bltm(0, 0, 1, 0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

        # Draw the stars.
        self.ui_stars.draw()

        # Draw all the game stuff on top of the black background
        self.game_handler.game_components.camera.draw(self.game_handler.levelhandler.curr_level.levelmap)

        # Sprites
        self.game_handler.game_components.game_sprites.draw()

        # Game UI components
        self.game_handler.game_components.game_ui.draw()

        # Statusbar
        self.game_handler.game_components.statusbar.draw()
    
    ###################
    # Object creation #
    ###################

    def init_sprites(self):
        self.sprites_factory = SpritesFactory(self.game_handler)
        sprites_handler = self.game_handler.game_components.game_sprites
        sprites_handler.append_sprites_handler(self.sprites_factory.create_sprite_handlers())
        sprites_handler.append_tilemap_sprites(self.sprites_factory.create_tilemap_sprites())
        sprites_handler.append_raw_sprites(self.sprites_factory.create_raw_sprites())
        self.assign_keybindings_to_sprites()

    def assign_keybindings_to_sprites(self):
        keybinds = self.game_handler.game_components.game_sprites.get_keybinds()
        self.game_handler.game_components.keylistener.append(keybinds)

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
        self.game_handler.game_components.game_sprites.restart_level()
        self.game_handler.game_components.game_ui.restart_level()

    def level_next(self):
        curr_level = self.game_handler.levelhandler.get_curr_lvl_idx()
        self.game_handler.levelhandler.set_lvl_by_idx(curr_level + 1)

        self.game_handler.game_components.game_sprites.init_level()
        self.game_handler.game_components.game_ui.init_level()
        self.level_restart()

    ##########################################################
    # All functions defined below are only used for TESTING. #
    ##########################################################
