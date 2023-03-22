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
from res.levels import levels
import game.sprites as sprites
import pyxel

class Game():
    def __init__(self):
        # Set up components
        # Make sure the keybind_setup is on the LAST list
        camera = base.Camera()
        soundplayer = base.SoundPlayer()
        keylistener = base.KeyListener()
        levelhandler = base.LevelHandler(levels)
        statusbar = base.Statusbar()
        self.game_collection = base.GameStateManager(soundplayer, camera, keylistener, levelhandler, statusbar)

        # Set up sprites
        self.sprites: dict[str, base.SpriteObj] = {}
        self.init_sprites()

        # Set up level
        self.game_collection.levelhandler.set_lvl(levels[0])

        # Set up keybindings
        self.keybinds_setup() 


    def scene_setup(self):
        pass

    def init_sprites(self):
        # Set up player
        fire = sprites.Flame()
        player = sprites.Player(self.game_collection, fire)
        self.sprites.update({"player": player})

    def keybinds_setup(self):
        """
        Initialize key listener.
        """

        objects_with_keybinds: dict[str, base.SpriteObj] = {
            "player": self.sprites["player"]
        }

        for o in objects_with_keybinds:
            try:
                self.game_collection.keylistener.append(o, objects_with_keybinds[o].keybindings)
            except AttributeError:
                continue

    def update(self):
        self.game_collection.keylistener.check()
    
    def draw_game_loop(self):
        self.game_collection.camera.draw(self.game_collection.levelhandler.curr_level.levelmap)

        for i in self.sprites:
            self.sprites[i].draw()
        

# Debugging
class Debugger:
    def __init__(self):
        pass
    
    def draw(self, player: sprites.Player, cam: base.Camera):
        pyxel.text(10, 10, f"player x: {player.coord.x}, player y: {player.coord.y}", pyxel.COLOR_WHITE)
        pyxel.text(10, 20, f"player x_map: {player.coord.x_map}, player y_map: {player.coord.y_map}", pyxel.COLOR_WHITE)
        pyxel.text(10, 30, f"cam x: {cam.x}, cam y: {cam.y}", pyxel.COLOR_WHITE)
        pyxel.text(10, 40, f"player x_vel: {player.x_vel}, y_vel: {player.y_vel}", pyxel.COLOR_WHITE)