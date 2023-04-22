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
from time import time
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
    TimerItem
)
from game.events import Event
from game.sprites.sprite_classes import Sprite, SpriteHandler, TilemapBasedSprite
from game.game_ui.game_ui_classes import UIComponent
from . import utils


# Keyboard handling
class KeyListener:
    """
    A Key listener to execute functions. Operates with an array like this:
    ```
    [
        {
            "a_function": KeyFunc,
            "other_function": KeyFunc
        } 
        { 
            "a_function": KeyFunc,
            "other_function": KeyFunc
        }
    ]
    ```
    A function name that is set to "none" will be treated as the function to be run when none of the keys bound are pressed.
    """

    def __init__(self):
        self.keys_to_check: list[dict[str, KeyFunc]] = []

    def add(self, keyfunc_dict: dict[str, KeyFunc]):
        """
        Add a new dict of `KeyFunc`s.
        """
        self.keys_to_check.append(keyfunc_dict)
    
    def append(self, keyfunc_list: list[dict[str, KeyFunc]]):
        """
        Append (extend) a new list of dict containing `KeyFunc`s.
        """
        self.keys_to_check.extend(keyfunc_list)

    def check(self):
        """
        Loop through key listeners and run function if key is pressed.
        """
        for i in self.keys_to_check:
            for key in i.values():
                if key.active:
                    match(key.btn_type):
                        case KeyTypes.BTN:
                            if pyxel.btn(key.binding):
                                key.func()
                        case KeyTypes.BTNP:
                            if pyxel.btnp(key.binding, hold=key.hold_time, repeat=key.repeat_time):
                                key.func()



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
class GameStatusbar:
    """
    Game statusbar which holds an array of items (`StatusBarItem`) to be displayed.
    """
    # The statusbar is being drawn constantly but not updated constantly.
    # The `update` method calls all function and stores it in an array of strings, which will be drawn
    # with the `draw` method.
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

    # XXX maybe a way to only update a particular statusbar item is useful.
    def update(self):
        """
        Update statusbar strings (call all functions used to get the string).
        """
        self.strings = [item.function() for item in self.items]

    def draw(self):
        """
        Draw statusbar.
        """
        if len(self.strings) > 0:
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
    def play(self, sfx: Sfx, loop: bool = False):
        """
        Play a sound (Sfx).
        """
        match(sfx.soundtype):
            case SoundType.AUDIO:
                pyxel.play(sfx.channel, sfx.idx, loop=loop)
            case SoundType.MUSIC:
                pyxel.playm(sfx.idx, loop=loop)

    def is_playing(self, sfx: Sfx) -> bool:
        if pyxel.play_pos(sfx.channel) == None:
            return False
        return True

    def stop_sfx_channel_playback(self, sfx: Sfx):
        pyxel.stop(sfx.channel)

    def stop_channel_playback(self, channel: int):
        pyxel.stop(channel)

# UI Components handling
class GameUI():
    """
    Handler for Game UIs.
    All UIs should be event-based, so there is no `update` method here.
    """
    def __init__(self):
        self.ui_components: dict[str, UIComponent] = {}
    
    def append(self, ui_components: dict[str, UIComponent]):
        self.ui_components.update(ui_components)
    
    def draw(self):
        [component.draw() for component in self.ui_components.values()]
    
    def init_level(self):
        [component.init_level() for component in self.ui_components.values()]
    
    def restart_level(self):
        [component.restart_level() for component in self.ui_components.values()]

# Sprites handling
class GameSprites:
    """
    Handler for sprites.
    """
    def __init__(self):
        self.init_slots()

    def init_slots(self):
        """
        Initialize all sprite slots. Also deletes all slots content.
        """
        self.sprites_handler: list[SpriteHandler] = []
        self.tilemap_sprites: list[TilemapBasedSprite] = []
        self.raw_sprites: list[Sprite] = []
    
    def append_sprites_handler(self, sprites_list: dict[str, SpriteHandler]):
        self.sprites_handler.extend(sprites_list.values())
    
    def append_tilemap_sprites(self, sprites_list: dict[str, TilemapBasedSprite]):
        self.tilemap_sprites.extend(sprites_list.values())
    
    def append_raw_sprites(self, sprites_list: dict[str, Sprite]):
        self.raw_sprites.extend(sprites_list.values())
    
    def update(self):
        """
        Update all sprites state.
        """
        [sprite.update() for sprite in self.sprites_handler]

    def draw(self):
        """
        Draw all sprites.
        """
        [sprite.draw() for sprite in self.sprites_handler]
    
    def init_level(self):
        """
        Function to be called on each new level.
        """
        [sprite.init_level() for sprite in self.sprites_handler]
        [sprite.init_level() for sprite in self.tilemap_sprites]

    def restart_level(self):
        """
        Function to be called after restarting a level.
        """
        [sprite.restart_level() for sprite in self.sprites_handler]
        [sprite.restart_level() for sprite in self.tilemap_sprites]

    def get_keybinds(self) -> list[dict[str, KeyFunc]]:
        """
        Get a list of dictionaries containing keybinds from all sprites that can be plugged into `KeyListener`.
        """

        keybinds: list[dict[str, KeyFunc]] = []
        keybinds.extend([sprite.keybindings for sprite in self.sprites_handler if sprite.keybindings])
        keybinds.extend([sprite.keybindings for sprite in self.raw_sprites if sprite.keybindings])
        keybinds.extend([sprite.keybindings for sprite in self.tilemap_sprites if sprite.keybindings])

        return keybinds
    
    def get_statusbars(self) -> list[StatusbarItem]:
        """
        Get an array of StatusbarItem from all sprites that can be plugged into `GameStatusBar`.
        """
        keybinds: list[StatusbarItem] = []
        [keybinds.extend(sprite.statusbar_items) for sprite in self.sprites_handler if sprite.statusbar_items]
        [keybinds.extend(sprite.statusbar_items) for sprite in self.raw_sprites if sprite.statusbar_items]
        [keybinds.extend(sprite.statusbar_items) for sprite in self.tilemap_sprites if sprite.statusbar_items]

        return keybinds


# Timer system
class Timer:
    """
    This timer provides a way to "wait" for a process without clogging up other processes, with precision up to 1s ÷ <game FPS>.
    """

    def __init__(self):
        self.time_start = time
        self.timer_items: list[TimerItem] = []
    
    def attach(self, limit: float) -> TimerItem:
        """
        Add a new function to run after waiting for `limit` seconds. This will return a `TimerItem`.
        Do NOT call this inside a game loop, as the timer will keep getting reinstantiated.

        Generally, you'd use this method like so:
        ```python
        Timer.attach(1).when_over(function_to_call)
        ```
        """

        timer_item = TimerItem(limit)
        self.timer_items.append(timer_item)
        return timer_item
    
    def update(self):
        """
        Update status of all items (`self.timer_items`).
        """
        for item in self.timer_items:
            if item.is_over():
                item.run_function()
                self.timer_items.remove(item)

# Text engine
# (kinda taken from https://github.com/kitao/pyxel/blob/main/python/pyxel/examples/13_bitmap_font.py because i'm not gonna figure out how BDFs work...)
# You know what, let's just ignore the text backend for now

# FIXME - Refactor later:
# - use classes instead of stupid dict[int, Optional[int], Optional[tuple[tuple[tupletupleblablabla]]]]

# Or just figure out another way, whatever.

# class Textengine:
#     BORDER_DIRECTIONS = [
#         (-1, -1),
#         (0, -1),
#         (1, -1),
#         (-1, 0),
#         (1, 0),
#         (-1, 1),
#         (0, 1),
#         (1, 1),
#     ]

#     def __init__(self, bdf_filename: str):
#         self.font_bounding_box = [0, 0, 0, 0]
#         self.fonts = self._parse_bdf(bdf_filename)
#         self.screen_ptr = pyxel.screen.data_ptr() # type: ignore
#         self.screen_width = pyxel.width

#     def _parse_bdf(self, bdf_filename: str):
#         fonts: dict[int, tuple[int, Optional[tuple[int]], Optional[list[int]]]] = {}
#         code: int = 0
#         bitmap: list[int] | None = None
#         dwidth = 0
#         bbx: tuple[int] | None = None
#         with open(bdf_filename, "r") as f:
#             for line in f:
#                 if line.startswith("FONTBOUNDINGBOX"):
#                     self.font_bounding_box = list(map(int, line.split()[1:]))
#                 elif line.startswith("ENCODING"):
#                     code = int(line.split()[1])
#                 elif line.startswith("DWIDTH"):
#                     dwidth = int(line.split()[1])
#                 elif line.startswith("BBX"):
#                     bbx = tuple(map(int, line.split()[1:]))
#                 elif line.startswith("BITMAP"):
#                     bitmap = []
#                 elif line.startswith("ENDCHAR"):
#                     fonts[code] = (
#                         dwidth,
#                         bbx,
#                         bitmap,
#                     )
#                     bitmap = None
#                 elif bitmap is not None:
#                     hex_string = line.strip()
#                     bin_string = bin(int(hex_string, 16))[2:].zfill(len(hex_string) * 4)
#                     bitmap.append(int(bin_string[::-1], 2))
#         return fonts

#     def _draw_font(self, x: int, y: int, font: dict[int, tuple[int, Optional[tuple[int]], Optional[list[int]]]] = {}, color: int):
#         dwidth, bbx, bitmap = font
#         screen_ptr = self.screen_ptr
#         screen_width = self.screen_width
#         x = x + self.font_bounding_box[2] + bbx[2]
#         y = y + self.font_bounding_box[1] + self.font_bounding_box[3] - bbx[1] - bbx[3]
#         for j in range(bbx[1]):
#             for i in range(bbx[0]):
#                 if (bitmap[j] >> i) & 1:
#                     screen_ptr[(y + j) * screen_width + x + i] = color

#     def draw_text(self, x, y, text, color=7, border_color=None, spacing=0):
#         for char in text:
#             code = ord(char)
#             if code not in self.fonts:
#                 continue
#             font = self.fonts[code]
#             if border_color is not None:
#                 for dx, dy in self.BORDER_DIRECTIONS:
#                     self._draw_font(
#                         x + dx,
#                         y + dy,
#                         font,
#                         border_color,
#                     )
#             self._draw_font(x, y, font, color)
#             x += font[0] + spacing

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
