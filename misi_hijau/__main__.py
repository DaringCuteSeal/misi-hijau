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
from core.common import WINDOW_HEIGHT, WINDOW_WIDTH
from game.game import Game
from res.resources_load import startup_load_resources

# Main App Class
class App:
    def __init__(self):
        """
        Initialize game.
        """
        # Pyxel stuff
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, capture_scale=8, title="Misi Hijau", fps=30, quit_key=pyxel.KEY_NONE)
        startup_load_resources()
        
        self.game = Game()

        # Run Pyxel!
        print("Selamat datang di Misi Hijau!")
        pyxel.run(self.update, self.draw)

    def update(self):
        """
        Update the state of the game.
        """
        self.game.update()

    def draw(self):
        """
        Render (draw) frame to screen.
        """
        self.game.draw()

if __name__ == "__main__":
    App()