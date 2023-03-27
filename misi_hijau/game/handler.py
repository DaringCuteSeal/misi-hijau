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

from dataclasses import dataclass
from .components import (
    SoundPlayer,
    Camera,
    KeyListener,
    LevelHandler,
    Statusbar,
    SpriteHandler,
    EventHandler,
)

# Manager of (almost) Everything here
@dataclass
class GameStateManager:
    """
    A set of game components.
    """
    soundplayer: SoundPlayer
    camera: Camera
    keylistener: KeyListener
    level_handler: LevelHandler
    statusbar: Statusbar
    sprite_handler: SpriteHandler
    event_handler: EventHandler

    def restart(self):
        self.sprite_handler.reset()
