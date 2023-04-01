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
Game components such as camera, sound player, key listener, etc.
"""

# Imports
import pyxel
from typing import Any, Callable
from dataclasses import dataclass

from .common import (
    KeyFunc,
    KeyTypes, 
    SoundType, 
    Sfx, 
    Level, 
    LevelMap, 
    StatusbarItem,
)
from game.events import Event
from game.sprites import Sprite
from game.ui import UIComponent
from game import utils

# Keyboard handling
class KeyListener:
    """
    A Key listener to execute functions. Operates with a dictionary like this:
    ```
    {
        "slot1": {
            "a_function": KeyFunc,
            "other_function": KeyFunc
        }
        "slot2": {
            "a_function": KeyFunc,
            "other_function": KeyFunc
        }
    }
    ```
    A function name that is set to "none" will be treated as the function to be run when none of the keys bound are pressed.
    """

    def __init__(self):
        self.checks: dict[str, dict[str, KeyFunc]] = {}

    def append(self, slot: str, keyfunc_dict: dict[str, KeyFunc]):
        """
        Append (update) list of key listeners.
        """
        self.checks[slot] = {}
        self.checks[slot].update(keyfunc_dict)

    def set_none_binding(self, slot: str, function: Callable[[], None]):
        """
        Assign a function to be executed when none of the keys from a slot was pressed.
        """
        if not self.checks[slot]["none"]:
            self.checks[slot]["none"] = KeyFunc(0, function, KeyTypes.BTN, True)

    def check(self):
        """
        Loop through key listeners and run function if key is pressed.
        """
        for slot in self.checks.values():
            no_key_pressed = True
            for key in slot.values():
                if key.active:
                    match(key.btn_type):
                        case KeyTypes.BTN:
                            if pyxel.btn(key.binding):
                                key.func()
                                no_key_pressed = False
                        case KeyTypes.BTNP:
                            if pyxel.btnp(key.binding, hold=key.hold_time, repeat=key.repeat_time):
                                key.func()
                                no_key_pressed = False
            if no_key_pressed and slot.get("none") and slot["none"].active:
                slot["none"].func()


# Level handling
class LevelHandler:
    """
    Handler for levels.
    """
    def __init__(self, levels: list[Level]):
        self.levels = levels
        self.curr_level: Level = levels[0]
    
    def set_lvl_by_idx(self, idx: int):
        level = self._find_level_by_idx(idx) 
        if level:
            self.curr_level = level

    def get_curr_lvl(self) -> Level:
        return self.curr_level

    def get_curr_lvl_idx(self) -> int:
        return self.curr_level.idx

    def _find_level_by_idx(self, idx: int) -> Level | None:
        for level in self.levels:
            if level.idx == idx:
                return level
    

# Camera handling
@dataclass
class Camera:
    """
    A 2D camera.
    """
    speed: float = 8
    x: float = 0
    y: float = 0
    # where the camera is heading; should be the same as player's vel variable. Only used by stars
    dir_x: float = 0
    dir_y: float = 0

    def __init__(self):
       pyxel.camera()
   
    def draw(self, levelmap: LevelMap):
        pyxel.bltm(0, 0, 0, self.x + utils.tile_to_real(levelmap.map_x), self.y + utils.tile_to_real(levelmap.map_y), 256, 256, pyxel.COLOR_BLACK)

# Statusbar handling
class Statusbar:
    """
    Game statusbar which holds an array of items (`StatusBarItem`) to be displayed.
    """
    def __init__(self):
        self.items: list[StatusbarItem] = []
        self.strings: list[str] = []
        self.def_x = pyxel.TILE_SIZE + 3
        self.def_y = 10
        self.def_gap_y = 8
    
    def append(self, items: list[StatusbarItem]):
        """
        Append (extend) an array of `StatusBarItem` to the statusbar's store.
        """
        self.items.extend(items)
        self._recalculate()
    
    def add(self, item: StatusbarItem):
        """
        Add a `StatusBarItem` to the statusbar's store.
        """
        self.items.append(item)
        self._recalculate()

    def clear(self):
        """
        Clear the statusbar.
        """
        self.items = []

    def update(self):
        """
        Update statusbar strings (call all functions used to get the string).
        """
        self.strings = [item.function() for item in self.items]

    def draw(self):
        """
        Draw statusbar.
        """
        for i, item in enumerate(self.items):
            string = self.strings[i]
            pyxel.text(item.x, item.y, string, item.color)
    
    def _recalculate(self):
        """
        Recalculate position for each statusbar item.
        """
        self.items = sorted(self.items, key=lambda x: x.idx)
        self.items[0].y = self.def_y
        self.items[0].x = self.def_x
        last_y = self.def_y

        for item in self.items[1:]:
            if item.custom_coords:
                continue
            item.x = self.def_x
            item.y = last_y + self.def_gap_y
            last_y = item.y

# Sound handling
@dataclass
class SoundPlayer():
    """
    A sound player.
    """
    def play(self, sfx: Sfx):
        """
        Play a sound (Sfx).
        """
        match(sfx.soundtype):
            case SoundType.AUDIO:
                pyxel.play(sfx.channel, sfx.idx, loop=sfx.loop)
            case SoundType.MUSIC:
                pyxel.playm(sfx.idx, loop=sfx.loop)
    def is_playing(self, sfx: Sfx) -> bool:
        if pyxel.play_pos(sfx.channel) == None:
            return False
        return True

# UI Components handling
class UIHandler():
    def __init__(self):
        self.ui_components: dict[str, UIComponent] = {}
    
    def append(self, ui_components: dict[str, UIComponent]):
        self.ui_components.update(ui_components)
    
    def draw(self):
        for component in self.ui_components.values():
            component.draw()

# Sprites handling
class SpriteHandler:
    """
    Handler for sprites.
    """
    def __init__(self):
        self.sprites: dict[str, Sprite] = {}
    
    def append(self, sprites: dict[str, Sprite]):
        """
        Append a dictionary of sprite into this sprite handler.
        """
        self.sprites.update(sprites)
    
    def update(self):
        """
        Update all sprites state.
        """
        for sprite in self.sprites.values():
            sprite.update()

    def draw(self):
        """
        Draw all sprites.
        """
        for sprite in self.sprites.values():
            sprite.draw()


# Event system
class EventHandler:
    """
    Event handling system.

    Operates with a dictionary like this:
    ```
    {
        "event_name": [HandlerFunction1, HandlerFunction2],
        "other_event_name": [HandlerFunction3]
    }
    ```

    Handler function may return a boolean if needed. It will be passed as the result of the `trigger_event` method for the event sender.
    """
    
    # i hate python function type checking =)
    def __init__(self):
        self._handlers: dict[str, list[Callable[..., bool | None]]] = {}
    
    def add_handler(self, event_name: str, handler: Callable[..., bool | None]):
        """
        Add a handler (subscribe) for an event.
        """
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        self._handlers[event_name].append(handler)
    
    def remove_handler(self, event_name: str, handler: Callable[..., Any]):
        """
        Remove a handler (unsubscribe) from an event.
        """
        if event_name in self._handlers:
            self._handlers[event_name].remove(handler)
    
    def trigger_event(self, event: Event) -> bool | None:
        """
        Trigger an event.
        """
        if event.name in self._handlers:
            results: list[bool | None] = []
            for handler in self._handlers[event.name]:
                if event.data:
                    results.append(handler(**event.data)) # pass data from Event to handler function as a dict
                else:
                    results.append(handler())

            # The value return is either "succeeded" or "failed", so if
            # there's a handler function that returned False, this
            # event trigger result should be False, and so on.

            if any(result is False for result in results):
                return False
            elif any(result is not None and result is not True for result in results):
                return None
            else:
                return True