# Copyright 2023 Cikitta Tjok

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from game import base
from game.sprites import Sprite, SpriteGroup, player, enemies, minerals
from res.levels import levels
import pyxel

class Game():
    def __init__(self):
        """
        Game initialization.
        """
        # Set up components
        # Make sure the keybind_setup is on the LAST list
        camera = base.Camera()
        soundplayer = base.SoundPlayer()
        keylistener = base.KeyListener()
        levelhandler = base.LevelHandler(levels)
        statusbar = base.Statusbar()
        self.game_collection = base.GameStateManager(soundplayer, camera, keylistener, levelhandler, statusbar)

        # Set up level
        self.game_collection.levelhandler.set_lvl(levels[0])

        # Set up sprites
        self.init_sprites()

        # Set up keybindings
        self.keybinds_setup() 


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
        # Stars need to be located at the back of everything, so we separate it.

        self.sprites_collection: dict[str, Sprite] = {
                # Order MATTERS.
                "player": player.Player(self.game_collection)
            }
        self.sprites = SpriteGroup(self.sprites_collection)

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

    def update(self):
        """
        Update game.
        """
        self.game_collection.keylistener.check()
    
    def draw_game_loop(self):
        """
        Draw game.
        """

        self.game_collection.camera.draw(self.game_collection.levelhandler.curr_level.levelmap)

        self.sprites.render()
        self.game_collection.statusbar.draw()


    
    ##########################################################
    # All functions defined below are only used for TESTING. #
    ##########################################################



# Debugging
class Debugger:
    def __init__(self, player: player.Player, game: base.GameStateManager):
        self.player = player
        self.cam = game.camera
        game.statusbar.add(base.StatusbarItem(self.draw, pyxel.COLOR_WHITE))
    
    def draw(self) -> str:
        return f"""
player x: {self.player.coord.x}, player y: {self.player.coord.y}
player x_map: {self.player.coord.x_map}, player y_map: {self.player.coord.y_map}
cam x: {self.cam.x}, cam y: {self.cam.y}
player x_vel: {self.player.x_vel}, y_vel: {self.player.y_vel}
"""