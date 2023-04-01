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

import pyxel
from math import sqrt # pyxel.sqrt(0) returns denormalized number; we need it to return 0.
from . import Sprite, SpriteCoordinate
from ..common import (
    ALPHA_COL,
    WINDOW_HEIGHT,
    Direction,
    KeyFunc,
    PlayerShipType,
    Sfx,
    SoundType,
    KeyTypes,
    StatusbarItem,
    Level
)
from ..game_handler import GameComponents
from .. import events
from ..utils import Ticker, tile_to_real

class Flame(Sprite):
    """
    A flame that's controlled by the player.
    """
    # The flame here is tightly coupled with the player but
    # this shouldn't be a problem as I kinda assume the player
    # and the flame is one single entity, just with 2 components
    def __init__(self):
        self.img = 0
        self.u = 32
        self.v = 16
        self.w = 16
        self.h = 8
        self.colkey = ALPHA_COL
        self.flames = [(32, 16), (32, 24)]
        self.coord = SpriteCoordinate(0, 0, 0, 0)
        self.ticker = Ticker(5)
    
    def draw(self):
        if self.ticker.get():
            self.set_costume(self.flames[pyxel.frame_count % 2])
        pyxel.blt(self.coord.x, self.coord.y, self.img, self.u, self.v, self.w, self.h, self.colkey)

    def update(self):
        self.hit_this_frame = False
        self.ticker.update()

    def flame_update(self, player_x: float, player_y: float, player_h: int):
        self.coord.x = player_x
        self.coord.y = player_y + player_h
    
class Player(Sprite):
    """
    Game player.
    """
    img = 0
    u = 32
    v = 0
    w = 16
    h = 16
    colkey = ALPHA_COL
    accel = 0.1
    drag = 0.04
    x_vel = 0
    y_vel = 0

    # Props for player that got attacked by an alien
    has_been_hit: bool = False
    hit_blink_count = 0
    hit_blink_idx = False


    soundbank = {
        "shoot": Sfx(SoundType.AUDIO, 3, 10),
        "attacked": Sfx(SoundType.AUDIO, 3, 14)
    }

    costumes = {
        "ship_1": (32, 0),
        "ship_2": (48, 16),
        "ship_3": (32, 32),

        # Costumes when player have been hurt by an alien
        "blink_ship_1": (0, 64),
        "blink_ship_2": (16, 64),
        "blink_ship_3": (32, 64)
    }

    def __init__(self, level: Level, game: GameComponents, health: int):
        self.keybindings = {
            "player_right": KeyFunc(pyxel.KEY_RIGHT, lambda: self.move_handler(Direction.RIGHT)),
            "player_left": KeyFunc(pyxel.KEY_LEFT, lambda: self.move_handler(Direction.LEFT)),
            "player_up": KeyFunc(pyxel.KEY_UP, lambda: self.move_handler(Direction.UP)),
            "player_down": KeyFunc(pyxel.KEY_DOWN, lambda: self.move_handler(Direction.DOWN)),
            "player_shoot": KeyFunc(pyxel.KEY_SPACE, lambda: self.shoot_handler(), KeyTypes.BTNP, hold_time=10, repeat_time=10),
        }

        self.statusbar_items = [
            StatusbarItem(100, self.get_speed, pyxel.COLOR_YELLOW),
        ]
            
        self.game = game

        self.level = level
        self.ship_type = level.ship_type
        levelmap = self.level.levelmap # only run ONCE; we don't want to get the level on every tick.
        self.level_width = tile_to_real(levelmap.level_width)
        self.level_height = tile_to_real(levelmap.level_height)

        self.health = health
        self.coord = SpriteCoordinate(self.level_width // 2, tile_to_real(4), self.level_width // 2, self.level_height - tile_to_real(4))
        
        self.statusbar = game.statusbar
        self.statusbar.append(self.statusbar_items)

        self.game.event_handler.add_handler(events.PlayerCollidingEnemy.name, self.is_colliding_with_enemy)
        self.game.event_handler.add_handler(events.LevelRestart.name, self.reset_handler)

        self.init_costume(self.ship_type)

        self.blinking_ticker = Ticker(10)
        self.speed_statusbar_ticker = Ticker(10)

        self.flame = Flame()

    def init_costume(self, ship_type: PlayerShipType):
        match ship_type:
            case PlayerShipType.SHIP1:
                self.set_costume(self.costumes["ship_1"])
            case PlayerShipType.SHIP2:
                self.set_costume(self.costumes["ship_2"])
            case PlayerShipType.SHIP3:
                self.set_costume(self.costumes["ship_3"])
    
    def switch_to_blink_costume(self, ship_type: PlayerShipType):
        match ship_type:
            case PlayerShipType.SHIP1:
                self.set_costume(self.costumes["blink_ship_1"])
            case PlayerShipType.SHIP2:
                self.set_costume(self.costumes["blink_ship_2"])
            case PlayerShipType.SHIP3:
                self.set_costume(self.costumes["blink_ship_3"])

    def move_handler(self, direction: Direction):

        match direction:
            case Direction.UP:
                self.y_vel -= self.accel
                self.coord.y_map -= self.accel
            case Direction.DOWN:
                self.y_vel += self.accel
                self.coord.y_map += self.accel
            case Direction.RIGHT:
                self.x_vel += self.accel
                self.coord.x_map += self.accel
            case Direction.LEFT:
                self.x_vel -= self.accel
                self.coord.x_map -= self.accel

    def move(self):
        self.game.event_handler.trigger_event(events.MineralsCheck(self.coord.x_map, self.coord.y_map, self.h))

        self.coord.x_map += self.x_vel
        self.coord.y_map += self.y_vel
        self.x_vel -= self.drag * self.x_vel
        self.y_vel -= self.drag * self.y_vel

        if self.coord.x_map < self.speed:
            self.coord.x_map = self.speed
        elif self.coord.x_map > self.level_width - self.w:
            self.coord.x_map = self.level_width - self.w
        else:
            self.game.event_handler.trigger_event(events.StarsScroll)
            

        if self.coord.y_map > self.level_height - self.h:
            self.coord.y_map = self.level_height - self.h
        elif self.coord.y_map < self.speed:
            self.coord.y_map = self.speed
        else:
            self.game.event_handler.trigger_event(events.StarsScroll)


    def cam_update(self):
        self.game.camera.y = self.coord.y_map

        if self.game.camera.y > self.level_height - WINDOW_HEIGHT // 2:
            self.game.camera.y = self.level_height - WINDOW_HEIGHT // 2
            self.game.camera.dir_y = 0
        elif self.game.camera.y < WINDOW_HEIGHT // 2:
            self.game.camera.y = WINDOW_HEIGHT // 2
            self.game.camera.dir_y = 0
        else:
            self.game.camera.dir_y = self.y_vel
            self.game.camera.dir_x = self.x_vel
        
    def update(self):
        self.map_to_view(self.game.camera.y)
        self.cam_update()
        self.flame.flame_update(self.coord.x, self.coord.y, self.h)
        self.speed_statusbar_ticker.update()

        self.move()

        if self.speed_statusbar_ticker.get():
            self.game.event_handler.trigger_event(events.UpdateStatusbar)

        if self.has_been_hit:
            if self.blinking_ticker.get():
                self.hit_blink_count += 1
                self.hit_blink_idx = not self.hit_blink_idx
            self.draw_if_hit()
            self.blinking_ticker.update()

        if not self.level.idx == 3:
            self.flame.ticker.update()
            self.flame.update()
        
        
    def draw_if_hit(self):

        if self.hit_blink_idx:
            self.switch_to_blink_costume(self.ship_type)
        else:
            self.init_costume(self.ship_type)

        if self.hit_blink_count == 8:
            self.hit_blink_count = 0
            self.has_been_hit = False
            self.init_costume(self.ship_type)

    def draw(self):
        self.flame.draw()
        pyxel.blt(self.coord.x, self.coord.y, self.img, self.u, self.v, self.w, self.h, self.colkey)

    
    # Event handler functions
    def shoot_handler(self):
        self.game.event_handler.trigger_event(events.PlayerShootBullets(self.coord.x_map, self.coord.y_map))
        self.game.soundplayer.play(self.soundbank["shoot"])
    
    def is_colliding_with_enemy(self, enemy_x: float, enemy_y: float, enemy_w: int, enemy_h: int) -> bool:
        if self.is_colliding(enemy_x, enemy_y, enemy_w, enemy_h):
            if not self.has_been_hit:
                self.game.event_handler.trigger_event(events.PlayerHealthChange(-1))
                self.health -= 1
                self.has_been_hit = True
                self.game.soundplayer.play(self.soundbank["attacked"])
            if self.health == 0:
                self.game.event_handler.trigger_event(events.LevelRestart)
                return True
        return False

    def reset_handler(self):
        self.coord.x_map = self.level_width // 2
        self.coord.y_map = self.level_height - tile_to_real(4)
        self.x_vel = 0
        self.y_vel = 0
        self.game.event_handler.trigger_event(events.PlayerHealthChange(self.level.max_health))
        self.health = self.level.max_health

    # Functions for statusbar
    def get_speed(self) -> str:
        magnitude = sqrt(self.y_vel * self.y_vel + self.x_vel * self.x_vel)
        magnitude = pyxel.floor(magnitude * 100)
        string = f"Speed: {magnitude} km/h"
        return string