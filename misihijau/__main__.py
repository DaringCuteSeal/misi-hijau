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
import sprites
import utils
import os

# Main App Class
class App:
    def __init__(self):
        """
        Initialize game.
        """
        # Pyxel stuff
        pyxel.init(utils.WINDOW_WIDTH, utils.WINDOW_HEIGHT, capture_scale=8, title="Misi Hijau")
        pyxel.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "res/res.pyxres"))

        # Set up components
        # Make sure the keybind_setup is on the LAST list
        self.debugger = Debugger()
        self.ticker = utils.Ticker()
        self.camera = utils.Camera()
        self.player = sprites.Player(self.camera, self.ticker)

        self.camera.speed = 2

        self.objects = [
            self.camera,
            self.player
        ]

        self.keybinds_setup()

        self.sound = utils.Sound(sprites.SoundBank)
        # Run Pyxel!
        pyxel.run(self.update, self.draw)

    def keybinds_setup(self):
        """
        Initialize key listener.
        """
        self.keylistener = utils.KeyListener()
        for o in self.objects:
            try:
                self.keylistener.append(o.keybindings)
            except AttributeError:
                continue

    def setup(self):
        """
        Setup initial scene.
        Anything that initializes the program and only run once should be put on __init__ instead.
        """

        self.camera.x = 0
        self.camera.y = 0

    def update(self):
        """
        Update the state of the game.
        """

        self.keylistener.check()
        self.ticker.update()

    def draw(self):
        """
        Render (draw) frame to screen.
        """
        for o in self.objects:
            o.draw()
        
        self.player.update_anim()
        
        self.debugger.draw(self.player, self.camera)
        

# 6: Debugging
class Debugger(App):
    def __init__(self):
        pass
    
    def draw(self, player, cam):
        pyxel.text(10, 10, f"player x: {player.coord.x}, player y: {player.coord.y}", pyxel.COLOR_WHITE)
        pyxel.text(10, 20, f"player x_map: {player.coord.x_map}, player y_map: {player.coord.y_map}", pyxel.COLOR_WHITE)
        pyxel.text(10, 30, f"cam x: {cam.x}, cam y: {cam.y}", pyxel.COLOR_WHITE)
        pyxel.text(10, 40, f"mouse x: {pyxel.mouse_x}, mouse y: {pyxel.mouse_y}", pyxel.COLOR_WHITE)
        pyxel.text(10, 50, f"player state: {player.state}", pyxel.COLOR_WHITE)

App() if __name__ == "__main__" else None