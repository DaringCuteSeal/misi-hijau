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

from game.common import WINDOW_HEIGHT, WINDOW_WIDTH, Level

from game.sprites import Sprite, player, bullets, enemy, minerals
from game.ui import UIComponent, stars, healthbar

from game import components
from game.game_handler import GameComponents, GameHandler

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
        statusbar = components.Statusbar()
        sprite_handler = components.SpriteHandler()
        event_handler = components.EventHandler()
        ui_handler = components.UIHandler()
        game_collection = GameComponents(soundplayer, camera, keylistener, statusbar, sprite_handler, event_handler, ui_handler)

        # Set up the main game handler
        level_handler = components.LevelHandler(levels)
        self.game_handler = GameHandler(level_handler, game_collection)
        self.game_handler.levelhandler.set_lvl_by_idx(1)

        # Set up level
        
        # Set up game UI components
        ui_components = self.create_ui_components()
        self.init_ui_components(ui_components)

        # Set up sprites
        sprites_collection = self.create_sprites(self.game_handler.levelhandler.get_curr_lvl())
        self.init_sprites(sprites_collection)

        # Debugging
        # self.debugger = Debugger(self.game_collection.sprite_handler.sprites["player"], self.game_collection)

    def scene_setup(self):
        """
        Scene initialization.
        """
        pass

    def create_ui_components(self) -> dict[str, UIComponent]:
        # We separate stars because it needs to be rendered before anything else
        self.ui_stars = stars.Stars(100, self.game_handler.game_components)

        ui_components: dict[str, UIComponent] = {
            "healthbar": healthbar.HealthBar(self.game_handler.game_components, self.game_handler.levelhandler.curr_level.max_health)
        }
        
        return ui_components

    def init_ui_components(self, ui_components: dict[str, UIComponent]):
        self.game_handler.game_components.ui_handler.append(ui_components)

    def create_sprites(self, level: Level) -> dict[str, Sprite]:
        # Set up player
        spr_bullets = bullets.Bullets(self.game_handler.game_components, level.bullet_color)
        spr_player = player.Player(level, self.game_handler.game_components, level.max_health)
        spr_enemies = enemy.EnemyHandler(level, enemy.EnemyType.ENEMY_1, self.game_handler.game_components)
        spr_minerals = minerals.MineralHandler(level, self.game_handler.game_components)

        sprites_collection: dict[str, Sprite] = {
                # Order matters (the layering)
                "bullets": spr_bullets,
                "enemies": spr_enemies,
                "player": spr_player,
                "minerals": spr_minerals
        }

        return sprites_collection

    def init_sprites(self, sprites_collection: dict[str, Sprite]):
        """
        Initialize game sprites.
        """

        self.game_handler.game_components.sprite_handler.append(sprites_collection)

        objects_with_keybinds: dict[str, Sprite] = {
            "player": sprites_collection["player"]
        }

        for o in objects_with_keybinds:
            try:
                self.game_handler.game_components.keylistener.append(o, objects_with_keybinds[o].keybindings)
            except AttributeError:
                continue
        
    def update(self):
        """
        Update game state.
        """
        self.game_handler.game_components.sprite_handler.update()
        self.ui_stars.update()
        self.game_handler.game_components.keylistener.check()
    
    def draw_game_loop(self):
        """
        Draw game scene.
        """

        # Draw the black background to prevent ghosting effect
        pyxel.bltm(0, 0, 0, 800, 800, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.ui_stars.draw()

        # Draw all the game stuff on top of the black background
        self.game_handler.game_components.camera.draw(self.game_handler.levelhandler.curr_level.levelmap)

        # And the sprites
        self.game_handler.game_components.sprite_handler.draw()

        # Statusbar
        self.game_handler.game_components.statusbar.draw()

        # And the rest of the game UI components
        self.game_handler.game_components.ui_handler.draw()

    
    ##########################################################
    # All functions defined below are only used for TESTING. #
    ##########################################################




# Debugging
class Debugger:
    def __init__(self, player: player.Player, game: GameComponents):
        self.player = player
        self.cam = game.camera
        game.statusbar.add(components.StatusbarItem(self.draw, pyxel.COLOR_WHITE))
    
    def draw(self) -> str:
#         return f"""
# player x: {self.player.coord.x}, player y: {self.player.coord.y}
# player x_map: {self.player.coord.x_map}, player y_map: {self.player.coord.y_map}
# cam x: {self.cam.x}, cam y: {self.cam.y}
# player x_vel: {self.player.x_vel}, y_vel: {self.player.y_vel}
# """
         return f"""
 player x: {pyxel.ceil(self.player.coord.x)}, player y: {pyxel.ceil(self.player.coord.y)}
 player x_map: {pyxel.ceil(self.player.coord.x_map)}, player y_map: {pyxel.ceil(self.player.coord.y_map)}
 cam x: {pyxel.ceil(self.cam.x)}, cam y: {pyxel.ceil(self.cam.y)}
 player x_vel: {pyxel.ceil(self.player.x_vel)}, y_vel: {pyxel.ceil(self.player.y_vel)}
"""