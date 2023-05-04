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
Game handler which holds game components and a level handler.
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

    # We have different loops for draw() and update() and they are dynamically settable.
    # This is useful so we can safe resource and organize game "scenes".
    # For example, we don't need to draw the (actual) game and update its state when we are just showing our intro to the player.
    callable_draw: Optional[Callable[[], None]] = None
    callable_update: Optional[Callable[[], None]] = None

    def set_callable_draw(self, loop: Callable[[], None] | None):
        self.callable_draw = loop

    def set_callable_update(self, loop: Callable[[], None] | None):
        self.callable_update = loop

    def draw(self):
        """
        Draw game scene.
        """
        self.callable_draw() if self.callable_draw else None
    
    def _core_update_loop(self):
        """
        Update important components.
        """
        self.game_components.keylistener.check()
        self.game_components.ticker.update()
        self.game_components.timer.update()

    def update(self):
        """
        Update game state.
        """
        self._core_update_loop()
        self.callable_update() if self.callable_update else None