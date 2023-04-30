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
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from .. import common

# Classes for UI Components

@dataclass
class UIComponentCoordinate:
    x: int = 0
    y: int = 0

class UIComponent(ABC):
    """
    A game UI Component.
    """
    img: int = 0
    u: int = 0
    v: int = 0
    w: int = 8
    h: int = 8
    active: bool = True
    keybindings: dict[str, common.KeyFunc] = field(default_factory=dict[str, common.KeyFunc])
    soundbank: dict[str, common.Sfx] = field(default_factory=dict[str, common.Sfx])
    costumes: dict[str, tuple[int, int]] = field(default_factory=dict[str, tuple[int, int]])
    coord: UIComponentCoordinate = UIComponentCoordinate(0, 0)

    @abstractmethod
    def _draw(self):
        """
        The actual draw method that needs to have an implementation.
        Will only be called if UI is active.
        """
    
    @abstractmethod
    def init_level(self):
        """
        Function to be called on every new level.
        """

    @abstractmethod
    def restart_level(self):
        """
        Function to be called after restarting a level.
        """

    def draw(self):
        """
        Draw (render) UI component.
        """
        
        self._draw() if self.active else None