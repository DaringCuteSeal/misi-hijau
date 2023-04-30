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
import os

PYXEL_RESOURCE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "res.pyxres")

IMG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")

SPLASH_SCREEN_IMAGE = os.path.join(IMG_PATH, "game_splash_screen.png")
INTRO_SLIDESHOW_IMAGE_PATH = os.path.join(IMG_PATH, "intro_slideshow_image")
INSTRUCTIONS_IMAGE_PATH = os.path.join(IMG_PATH, "instructions.png")

# FONT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "font", "PIXELADE.ttf")

def startup_load_resources():
    pyxel.load(PYXEL_RESOURCE_PATH)
    pyxel.image(1).load(0, 0, SPLASH_SCREEN_IMAGE)