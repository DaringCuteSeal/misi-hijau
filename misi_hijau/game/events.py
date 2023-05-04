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
Definition for game events.
"""

import pyxel

from dataclasses import dataclass
from typing import Callable, Optional, Any

@dataclass
class Event:
    """
    An event. May include an optional dictionary that will be passed as argument(s) to the handler function when triggered.
    """
    name: str
    data: Optional[dict[str, Any]] = None

# Events with data being passed
@dataclass
class PlayerShootBullets(Event):
    def __init__(self, player_x: float, player_y: float):
        self.data = {
            "player_x": player_x,
            "player_y": player_y
        }
    name = "player_shoot_bullets"

class BulletsCheck(Event):
    name = "bullets_check"
    def __init__(self, enemy_x: float, enemy_y: float, enemy_w: float, enemy_h: int):
        self.data = {
            "enemy_x_map": enemy_x,
            "enemy_y_map": enemy_y,
            "enemy_w": enemy_w,
            "enemy_h": enemy_h
        }

class PlayerCollidingEnemy(Event):
    name = "is_player_colliding_enemy"
    def __init__(self, enemy_x: float, enemy_y: float, enemy_w: float, enemy_h: int):
        self.data = {
            "enemy_x": enemy_x,
            "enemy_y": enemy_y,
            "enemy_w": enemy_w,
            "enemy_h": enemy_h
        }

class MineralsCheck(Event):
    name = "minerals_check"
    def __init__(self, player_x_map: float, player_y_map: float, player_h: int):
        self.data = {
            "player_x_map": player_x_map,
            "player_y_map": player_y_map,
            "player_h": player_h
        }

class PlayerHealthChange(Event):
    name = "player_health_change"
    def __init__(self, value: int):
        self.data = {
            "change_value": value
        }

class AppendBlastEffect(Event):
    name = "append_blast_effect"
    def __init__(self, x: float, y: float, object_w: int, object_h: int):
        self.data = {
            "x": x,
            "y": y,
            "object_w": object_w,
            "object_h": object_h
        }

class FlameUpdate(Event):
    name = "flame_update"
    def __init__(self, x: float, y: float, h: int):
        self.data = {
            "player_x": x,
            "player_y": y,
            "player_h": h
        }
        
class TilemapPlayerCheck(Event):
    name = "tilemap_player_check"
    def __init__(self, uv: tuple[int, int], tile_x: int, tile_y: int):
        self.data = {
            "uv": uv,
            "tile_x": tile_x,
            "tile_y": tile_y
        }

class BroadcastEnemiesCount(Event):
    name = "broadcast_enemies_count"
    def __init__(self, count: int):
        self.data = {
            "count": count
        }

# Event-based UI components
class ShowBlinkingTextHint(Event):
    name = "show_blinking_text_hint"
    def __init__(self, x: int, y: int, msg: str, background_img_idx: int):
        self.data = {
            "x": x,
            "y": y,
            "msg": msg,
            "background_img_idx": background_img_idx
        }

HideBlinkingTextHint = Event("hide_blinking_text_hint")

class ShowDialog(Event):
    name = "show_dialog"
    def __init__(self,
                 message: str,
                 width: int,
                 text_gap: int,
                 text_color: int,
                 bg_color: int,
                 function_when_done: Optional[Callable[..., Any]] = None,
                 key_dismiss: int = pyxel.KEY_SPACE,
                 sfx: bool = False,
                 show_dismiss_msg: bool = True,
                 dismiss_msg_col: int = pyxel.COLOR_GRAY,
                 dismiss_msg_str: str = "UNDEFINED"):

        self.data = {
            "message": message,
            "width": width,
            "text_gap": text_gap,
            "text_color": text_color,
            "bg_color": bg_color,
            "function_when_done": function_when_done,
            "key_dismiss": key_dismiss,
            "sfx": sfx,
            "show_dismiss_msg": show_dismiss_msg,
            "dismiss_msg_col": dismiss_msg_col,
            "dismiss_msg_str": dismiss_msg_str
        }

# Events without data being passed
TextengineInterrupt = Event("text_engine_interrupt") # stop currently running text engine
CheckLevelComplete = Event("check_level_complete") # check whether or not level has been completed
UpdateHealthbar = Event("update_healthbar")
UpdateStatusbar = Event("update_statusbar")
SlideshowNext = Event("slideshow_next") # next game intro slide
ShowInstructions = Event("show_instruction") # show game instruction
StarsScroll = Event("stars_scroll")
StartGame = Event("start_game") # start game
LevelRestart = Event("restart_level") # restart level
LevelNext = Event("level_next") # switch to next level
ActivateLevel = Event("activate_level") # activate keybinds or other things in level
ShowLevelStats = Event("show_level_stats")