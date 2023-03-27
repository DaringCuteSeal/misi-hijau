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

# Imports
import pyxel
import os
from game.common import WINDOW_HEIGHT, WINDOW_WIDTH
from game.setup_components import Game

# Main App Class
class App:
    def __init__(self):
        """
        Initialize game.
        """
        # Pyxel stuff
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, capture_scale=8, title="Misi Hijau")
        pyxel.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "res/res.pyxres"))

        self.game = Game()

        # Run Pyxel!
        print("Selamat datang di Misi Hijau!")
        pyxel.run(self.update, self.draw)


    def setup(self):
        """
        Setup initial scene.
        Anything that initializes the program and only run once should be put on game.__init__ instead.
        """
        self.game.scene_setup()

    def update(self):
        """
        Update the state of the game.
        """
        self.game.update()

    def draw(self):
        """
        Render (draw) frame to screen.
        """
        self.game.draw_game_loop()
    


if __name__ == "__main__":
    App()