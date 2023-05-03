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

"""
Game handler which holds game components.
"""

from dataclasses import dataclass
from typing import Callable, Optional
from .components import (
    SoundPlayer,
    Camera,
    KeyListener,
    LevelHandler,
    GameStatusbar,
    GameSprites,
    EventHandler,
    GameUI,
    TickerHandler,
    Timer
)

@dataclass
class GameComponents:
    """
    A set of game components.
    """
    soundplayer: SoundPlayer
    camera: Camera
    keylistener: KeyListener
    statusbar: GameStatusbar
    game_sprites: GameSprites
    game_ui: GameUI
    event_handler: EventHandler
    ticker: TickerHandler
    timer: Timer

# Manager of (almost) Everything here
@dataclass
class GameHandler:
    """
    Master game handler.
    """
    levelhandler: LevelHandler
    game_components: GameComponents
    callable_draw: Optional[Callable[..., None]]