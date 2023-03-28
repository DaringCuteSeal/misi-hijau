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

from game import components
from game.sprites import Sprite, SpriteHandler, player, bullets, enemy, stars, minerals
from game.game_handler import GameStateManager
from res.levels import levels
import pyxel

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
        level_handler = components.LevelHandler(levels)
        statusbar = components.Statusbar()
        sprite_handler = components.SpriteHandler()
        event_handler = components.EventHandler()
        self.game_collection = GameStateManager(soundplayer, camera, keylistener, level_handler, statusbar, sprite_handler, event_handler)

        # Set up level
        self.game_collection.level_handler.set_lvl(levels[0])

        # Set up sprites
        sprites_collection = self.create_sprites()
        self.init_sprites(sprites_collection)
        # self.debugger = Debugger(self.game_collection.sprite_handler.sprites["player"], self.game_collection)

    def scene_setup(self):
        """
        Scene initialization.
        """
        pass

    def create_sprites(self) -> dict[str, Sprite]:
        # Set up player
        spr_bullets = bullets.Bullets(self.game_collection)
        spr_player = player.Player(self.game_collection)
        spr_enemies = enemy.EnemyHandler(enemy.EnemyType.ENEMY_1, self.game_collection)
        spr_stars = stars.Stars(100, self.game_collection)
        spr_minerals = minerals.MineralHandler(self.game_collection)

        sprites_collection: dict[str, Sprite] = {
                # Order MATTERS.
                "stars": spr_stars,
                "bullets": spr_bullets,
                "player": spr_player,
                "enemies": spr_enemies,
                "minerals": spr_minerals
        }

        return sprites_collection


    def init_sprites(self, sprites_collection: dict[str, Sprite]):
        """
        Initialize game sprites.
        """

        self.game_collection.sprite_handler.append(sprites_collection)

        objects_with_keybinds: dict[str, Sprite] = {
            "player": sprites_collection["player"]
        }

        for o in objects_with_keybinds:
            try:
                self.game_collection.keylistener.append(o, objects_with_keybinds[o].keybindings)
            except AttributeError:
                continue
        
    def update(self):
        """
        Update game.
        """
        self.game_collection.sprite_handler.update()
        self.game_collection.keylistener.check()
    
    def draw_game_loop(self):
        """
        Draw game.
        """

        self.game_collection.camera.draw(self.game_collection.level_handler.curr_level.levelmap)
        self.game_collection.sprite_handler.draw()
        self.game_collection.statusbar.draw()


    
    ##########################################################
    # All functions defined below are only used for TESTING. #
    ##########################################################



# Debugging
class Debugger:
    def __init__(self, player: player.Player, game: GameStateManager):
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