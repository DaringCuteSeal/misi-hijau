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

# Imports
import pyxel
import game.sprites as sprites
import game.base as base
from game.levels import levels
import os

# Main App Class
class App:
    def __init__(self):
        """
        Initialize game.
        """
        # Pyxel stuff
        pyxel.init(base.WINDOW_WIDTH, base.WINDOW_HEIGHT, capture_scale=8, title="Misi Hijau")
        pyxel.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "res/res.pyxres"))

        # Set up components
        # Make sure the keybind_setup is on the LAST list
        self.debugger = Debugger()
        ticker = base.Ticker()
        camera = base.Camera()
        soundplayer = base.SoundPlayer()
        keylistener = base.KeyListener()
        levelhandler = base.LevelHandler(levels)
        self.game = base.GameStateManager(soundplayer, camera, ticker, keylistener, levelhandler)

        # Set up level
        self.game.levelhandler.curr_level = levels[0]
        # Set up sprites
        self.player = sprites.Player(self.game)

        # Set up keybindings
        self.keybinds_setup()

        # Run Pyxel!
        pyxel.run(self.update, self.draw)

    def keybinds_setup(self):
        """
        Initialize key listener.
        """

        self.objects = {
            "player": self.player
        }

        for o in self.objects:
            try:
                self.game.keylistener.append(o, self.objects[o].keybindings)
            except AttributeError:
                continue

    def setup(self):
        """
        Setup initial scene.
        Anything that initializes the program and only run once should be put on __init__ instead.
        """

        pass

    def update(self):
        """
        Update the state of the game.
        """

        self.game.keylistener.check()
        self.game.ticker.update()

    def draw(self):
        """
        Render (draw) frame to screen.
        """
        for o in self.objects:
            self.objects[o].draw()
        
        self.game.camera.draw(self.game.levelhandler.curr_level.levelmap)
        self.player.draw()
        self.debugger.text(self.player, self.game.camera)
        

# Debugging
class Debugger(App):
    def __init__(self):
        pass
    
    def text(self, player: sprites.Player, cam: base.Camera):
        pyxel.text(10, 10, f"player x: {player.coord.x}, player y: {player.coord.y}", pyxel.COLOR_WHITE)
        pyxel.text(10, 20, f"player x_map: {player.coord.x_map}, player y_map: {player.coord.y_map}", pyxel.COLOR_WHITE)
        pyxel.text(10, 30, f"cam x: {cam.x}, cam y: {cam.y}", pyxel.COLOR_WHITE)
        pyxel.text(10, 40, f"player x_vel: {player.x_vel}, y_vel: {player.y_vel}", pyxel.COLOR_WHITE)

App() if __name__ == "__main__" else None