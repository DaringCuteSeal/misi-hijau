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
from game.sprites import Sprite, SpriteHandler, player, bullets, enemy
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
        levelhandler = components.LevelHandler(levels)
        statusbar = components.Statusbar()
        self.game_collection = components.GameStateManager(soundplayer, camera, keylistener, levelhandler, statusbar)

        # Set up level
        self.game_collection.levelhandler.set_lvl(levels[0])

        # Set up sprites
        self.init_sprites()

        # Set up keybindings
        self.keybinds_setup() 

        # self.debugger = Debugger(self.sprites_collection["player"], self.game_collection) #type: ignore


    def scene_setup(self):
        """
        Scene initialization.
        """
        pass

    def init_sprites(self):
        """
        Initialize game sprites.
        """
        # Set up player
        spr_bullets = bullets.Bullets(self.game_collection.camera)
        spr_player = player.Player(self.game_collection, spr_bullets)
        spr_enemies = enemy.EnemyGroup(enemy.EnemyType.ENEMY_1, self.game_collection, spr_player, spr_bullets)

        self.game_collection.statusbar.add(components.StatusbarItem(spr_player.get_speed, pyxel.COLOR_YELLOW)) # XXX testing only
        # plz fix statusbar :) :) :)

        self.sprites_collection: dict[str, Sprite] = {
                # Order MATTERS.
                "bullets": spr_bullets,
                "player": spr_player,
                "enemies": spr_enemies
            }
        self.sprites_handler = SpriteHandler(self.sprites_collection, self.game_collection)

    def keybinds_setup(self):
        """
        Initialize key listener.
        """

        objects_with_keybinds: dict[str, Sprite] = {
            "player": self.sprites_collection["player"]
        }

        for o in objects_with_keybinds:
            try:
                self.game_collection.keylistener.append(o, objects_with_keybinds[o].keybindings)
            except AttributeError:
                continue
        
        test = {
            "test": components.KeyFunc(pyxel.KEY_R, lambda: self.sprites_handler.reset(), components.KeyTypes.BTNP)
        }
        self.game_collection.keylistener.append("test", test)

    def update(self):
        """
        Update game.
        """
        self.sprites_handler.update()
        self.game_collection.keylistener.check()
    
    def draw_game_loop(self):
        """
        Draw game.
        """

        self.game_collection.camera.draw(self.game_collection.levelhandler.curr_level.levelmap)
        self.sprites_handler.render()


    
    ##########################################################
    # All functions defined below are only used for TESTING. #
    ##########################################################



# Debugging
class Debugger:
    def __init__(self, player: player.Player, game: components.GameStateManager):
        self.player = player
        self.cam = game.camera
        game.statusbar.add(components.StatusbarItem(self.draw, pyxel.COLOR_WHITE))
    
    def draw(self) -> str:
        return f"""
player x: {self.player.coord.x}, player y: {self.player.coord.y}
player x_map: {self.player.coord.x_map}, player y_map: {self.player.coord.y_map}
cam x: {self.cam.x}, cam y: {self.cam.y}
player x_vel: {self.player.x_vel}, y_vel: {self.player.y_vel}
"""