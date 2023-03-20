# Copyright 2023 Cikitta Tjok

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

### Utilities for a better workflow

# Imports
import pyxel
from typing import Callable, Optional
from enum import Enum
from dataclasses import dataclass, field

# Enums
class Direction(Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3

class SoundType(Enum):
    AUDIO = 0
    MUSIC = 1

class PlayerShip(Enum):
    SHIP1 = 0
    SHIP2 = 1
    SHIP3 = 2

# Other Constants
ALPHA_COL = pyxel.COLOR_PURPLE
WINDOW_WIDTH = 256
WINDOW_HEIGHT = 256
TILE_SIZE = 8

# Keyboard handling
class KeyTypes(Enum):
    BTN = 0
    BTNP = 1

@dataclass
class KeyFunc:
    """
    An object with a key and its associated function.
    """
    binding: int
    func: Callable[[], None]
    btn_type: KeyTypes = KeyTypes.BTN
    active: bool = True
    hold_time: Optional[int] = None
    repeat_time: Optional[int] = None


class KeyListener:
    """
    A Key listener to execute functions. Operates in a dictionary like this:
    {
        "slotname": {
            "function_name": KeyFunc
        }
    }
    A function name that is set to "none" will be treated as the function to be run when none of the keys bound are pressed.
    """

    def __init__(self):
        self.checks: dict[str, dict[str, KeyFunc]] = {}

    def append(self, slot: str, keyfunc_dict: dict[str, KeyFunc]):
        """
        Append list of key listeners.
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
@dataclass
class LevelMap:
    """
    A level map. All values are in tilemap scale (TILE_SIZE)
    """
    map_x: int # Offset x of tilemap
    map_y: int # Offset y of tilemap
    level_width: int
    level_height: int

@dataclass
class Level:
    """
    A level.
    """
    idx: int
    ship: PlayerShip
    levelmap: LevelMap

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

    def __init__(self):
       pyxel.camera()
   
    def draw(self, levelmap: LevelMap):
        pyxel.bltm(0, 0, 0, self.x + levelmap.map_x, self.y + levelmap.map_y, 256, 256)


# Text handling
# TODO

# Tick handling
# XXX An entity SHOULD have their own ticker. If there's only one GLOBAL ticker, everything would be messed up.
class Ticker:
    """
    Retro games aren't meant to be smooth. However, Pyxel supports high frame rate. This timer can be used to limit a rate of something without messing with the game's actual FPS.
    """
    def __init__(self, frame_limit: float):
        """
        Initialize a new tick timer for an entity.
        """
        self.time_since_last_move = 0
        self.time_last_frame = 0
        self.limit = frame_limit
    
    def update(self):
        """
        Update tick counts. Should be run on every game tick by sprite.
        """
        time_this_frame = pyxel.frame_count
        self.dt = time_this_frame - self.time_last_frame
        self.time_last_frame = time_this_frame
        self.time_since_last_move += self.dt
    
    def get(self) -> bool:
        """
        Get status of tick.
        """
        
        if self.time_since_last_move * 10 >= self.limit * 10:
            self.time_since_last_move = 0
            return True
        return False

# Sound handling
@dataclass
class Sfx():
    soundtype: SoundType
    channel: int
    index: int = 0
    loop: bool = False

@dataclass
class SoundPlayer():
    ch: int = 0

    def play(self, bank: dict[str, Sfx], name: str):
        """
        Play a sound from soundbank.
        """
        match(bank[name].soundtype):
            case SoundType.AUDIO:
                pyxel.play(self.ch, bank[name].index, loop=bank[name].loop)
            case SoundType.MUSIC:
                pyxel.playm(bank[name].index, loop=bank[name].loop)


# Sprites handling
@dataclass
class Coordinate:
    # ↓ needs to be float because we use smooth movements and accels/decels might need to use decimal numbers.
    x: float = 0
    y: float = 0
    x_map: float = 0
    y_map: float = 0

@dataclass
class SpriteObj:
    """
    A sprite object class with some predefined functions to make costume handling easier.
    """
    coord: Coordinate
    img: int = 0
    u: int = 0
    v: int = 0
    w: int = 8
    h: int = 8
    speed: float = 1
    colkey: int | None = None
    costume_i: int = 0
    keybindings: dict[str, KeyFunc] = field(default_factory=dict[str, KeyFunc])
    soundbank: dict[str, Sfx] = field(default_factory=dict[str, Sfx])
    costumes: dict[str, tuple[int, int]] = field(default_factory=dict[str, tuple[int, int]])

    def draw(self):
        """
        Draw (render) character.
        """
        pyxel.blt(self.coord.x, self.coord.y, self.img, self.u, self.v, self.w, self.h, self.colkey)
    
    def set_costume(self, costume: tuple[int, int]):
        """
        Set costume based on spritemap coordinate.
        """
        self.u = costume[0]
        self.v = costume[1]

    def costume_toggle(self, costume_1: tuple[int, int], costume_2: tuple[int, int]):
        """
        Set costume based on current alternating costume index.
        """
        if self.costume_i:
            self.costume = costume_1
        else:
            self.costume = costume_2

# Manager of (almost) Everything here
@dataclass
class GameStateManager:
    """
    A set of game components.
    """
    soundplayer: SoundPlayer
    camera: Camera
    keylistener: KeyListener
    levelhandler: LevelHandler

# Functions
def map_to_view(sprite: SpriteObj, camera_pos: tuple[float, float]) -> tuple[float, float] | bool:
    """
    Get position of object in screen based on its position on the map. Returns `False` if object is not within the camera boundary.
    """

    screen_x = sprite.coord.x_map - camera_pos[0]
    screen_y = sprite.coord.y_map - camera_pos[1]

    if screen_x < 0 or screen_x > WINDOW_WIDTH or screen_y < 0 or screen_y > WINDOW_HEIGHT:
        return False

    return (screen_x, screen_y)

def tile_to_real(size: int) -> int:
    """
    Get real tile size from a tilemap scale.
    """
    return size * TILE_SIZE

def round_to_tile(size: int) -> int:
    return pyxel.ceil(size / TILE_SIZE) * TILE_SIZE