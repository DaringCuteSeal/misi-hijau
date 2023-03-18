# Copyright 2023 Cikitta Tjok

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
        self.player = sprites.Player()
        self.camera = utils.Camera(self.player)

        self.camera.speed = 2

        self.objects = [
            self.camera,
            self.player
        ]

        self.keybinds_setup()

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

App() if __name__ == "__main__" else None