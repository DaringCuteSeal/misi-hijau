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
from typing import Optional, Any

@dataclass
class Event:
    """
    An event. May include an optional dictionary that will be passed as an argument to the handler function.
    """
    name: str
    data: Optional[dict[str, Any]]

# Events with data being passed
class PlayerShootBullets(Event):
    name = "player_shoot_bullets"
    def __init__(self, player_x: float, player_y: float):
        self.data = {
            "player_x": player_x,
            "player_y": player_y
        }

class BulletsCheck(Event):
    name = "bullets_check"
    def __init__(self, enemy_x: float, enemy_y: float, enemy_w: float, enemy_h: float):
        self.data = {
            "enemy_x": enemy_x,
            "enemy_y": enemy_y,
            "enemy_w": enemy_w,
            "enemy_h": enemy_h
        }


# Events without data being passed
StarsScroll = Event("stars_scroll", None)
LevelRestart = "level_restart"