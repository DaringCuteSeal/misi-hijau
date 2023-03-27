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
        for slot in self.checks:
            no_key_pressed = True
            for key in self.checks[slot].values():
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
            if no_key_pressed and self.checks[slot].get("none") and self.checks[slot]["none"].active:
                self.checks[slot]["none"].func()


# Level handling
class LevelHandler:
    """
    Handler for levels.
    """
    def __init__(self, levels: list[Level]):
        self.levels = levels
        self.curr_level = levels[0]
    
    def set_lvl(self, level: Level):
        self.curr_level = level

    def get_curr(self) -> Level:
        return self.curr_level

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
        pyxel.bltm(0, 0, 0, self.x + utils.tile_to_real(levelmap.map_x), self.y + utils.tile_to_real(levelmap.map_y), 256, 256)


# Statusbar handling
class Statusbar:
    """
    Game statusbar which holds an array of items (`StatusBarItem`) to be displayed.
    """
    def __init__(self):
        self.items: list[StatusbarItem] = []
        self.def_x = utils.TILE_SIZE + 3
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

    def draw(self):
        """
        Draw statusbar.
        """
        for item in self.items:
            string = item.function()
            pyxel.text(item.x, item.y, string, item.color)
    
    def _recalculate(self):
        """
        Recalculate position for each statusbar item.
        """
        self.items[0].y = self.def_y
        self.items[0].x = self.def_x
        last_y = -self.def_gap_y + self.def_y

        for item in self.items[1:]:
            item.x = self.def_x
            item.y = last_y + self.def_gap_y

# Sound handling
@dataclass
class SoundPlayer():
    ch: int = 0

    def play(self, sfx: Sfx):
        """
        Play a sound from soundbank.
        """
        match(sfx.soundtype):
            case SoundType.AUDIO:
                pyxel.play(self.ch, sfx.index, loop=sfx.loop)
            case SoundType.MUSIC:
                pyxel.playm(sfx.index, loop=sfx.loop)

# Sprites handling
class SpriteHandler:
    """
    Handler for sprites.
    """
    def __init__(self):
        self.sprites: dict[str, Sprite] = {}
    
    def append(self, sprites: dict[str, Sprite]):
        self.sprites.update(sprites)
    
    def update(self):
        for i in self.sprites:
            self.sprites[i].update()

    def render(self):
        for i in self.sprites:
            self.sprites[i].draw()

    def reset(self):
        for i in self.sprites:
            self.sprites[i].reset()



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
    def __init__(self):
        self._handlers: dict[str, list[Callable[..., bool | None]]] = {}
    
    def add_handler(self, event_name: str, handler: Callable[..., bool | None]):
        """
        Add a handler (subscribe) for a particular event name.
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
            for handler in self._handlers[event.name]:
                if event.data:
                    return(handler(**event.data))
                else:
                    return(handler())
