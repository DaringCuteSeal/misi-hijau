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

from misi_hijau.res.storyline_text import story_text

from ..game_handler import GameHandler
from res.resources_load import INTRO_SLIDESHOW_IMAGE_PATH, SPLASH_SCREEN_IMAGE
from ..common import WINDOW_HEIGHT, KeyFunc, Sfx, SoundType
from .text_engine import TextEngine
from .. import events

class Instruction