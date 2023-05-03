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
from core.sprite_classes import Sprite, SpriteCoordinate, SpriteHandler
from core.common import (
    ALPHA_COL,
    WINDOW_HEIGHT,
    Direction,
    KeyFunc,
    PlayerShipType,
    Sfx,
    SoundType,
    KeyTypes,
    TextStatusbarItem,
    MAP_Y_OFFSET_TILES
)
from core.game_handler import GameHandler
from .. import events
from core.utils import tile_to_real, real_to_tile, hypotenuse

class Flame(Sprite):
    """
    A flame that's controlled by the player.
    """
    # The flame here is tightly coupled with the player but
    # this shouldn't be a problem as I kinda assume the player
    # and the flame is one single entity, just with 2 components
    def __init__(self, game_handler: GameHandler):
        self.img = 0
        self.u = 32
        self.v = 16
        self.w = 16
        self.h = 8
        self.colkey = ALPHA_COL
        self.flames = [(32, 16), (32, 24)]
        self.coord = SpriteCoordinate(0, 0, 0, 0)
        self.ticker = game_handler.game_components.ticker.attach(5)
        game_handler.game_components.event_handler.add_handler(events.FlameUpdate.name, self.flame_update)
    
    def draw(self):
        pyxel.blt(self.coord.x, self.coord.y, self.img, self.u, self.v, self.w, self.h, self.colkey)

    def update(self):
        self.hit_this_frame = False

        if self.ticker.get():
            self.set_costume(self.flames[pyxel.frame_count % 2])

    def flame_update(self, player_x: float, player_y: float, player_h: int):
        self.coord.x = player_x
        self.coord.y = player_y + player_h
    
    def level_reset(self):
        pass
    
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
    accel = 0.2
    drag = 0.09

    # Props for player that got attacked by an alien
    has_been_hit: bool = False
    hit_blink_count = 0
    hit_blink_idx = False


    soundbank = {
        "attacked": Sfx(SoundType.AUDIO, 0, 14)
    }

    costumes = {
        "ship_1": (32, 0),
        "ship_2": (48, 16),
        "ship_3_1": (32, 32),
        "ship_3_2": (48, 32),

        # Costumes when player have been hurt by an alien
        "blink_ship_1": (0, 64),
        "blink_ship_2": (16, 64),
        "blink_ship_3": (32, 64)
    }

    def __init__(self, game_handler: GameHandler):

        self.game = game_handler

        self.coord = SpriteCoordinate(0, 0, 0, 0)
        self.blinking_ticker = self.game.game_components.ticker.attach(10)
        self.speed_statusbar_ticker = self.game.game_components.ticker.attach(10)

        self.player_setup()
        self.setup_event_handlers()
    
    def setup_event_handlers(self):
        self.game.game_components.event_handler.add_handler(events.PlayerCollidingEnemy.name, self.is_colliding_with_enemy)

    def player_setup(self):
        """
        Get level and then initiate player based on the level.
        """
        self.x_vel = 0
        self.y_vel = 0

        self.level = self.game.levelhandler.get_curr_lvl()

        self.ship_type = self.level.ship_type
        levelmap = self.level.levelmap # only run ONCE; we don't want to get the level on every tick.
        self.level_width = tile_to_real(levelmap.level_width)
        self.level_height = tile_to_real(levelmap.level_height)

        self.health = self.level.max_health
        self.reset_coord() # don't reinstantiate or else we will break bound values
        self.map_to_view(self.game.game_components.camera.y)

        if self.level.idx:
            self.ship3_costume_ticker = self.game.game_components.ticker.attach(5)
            self.ship3_costume_idx = False

        self.init_costume(self.ship_type)

    def reset_coord(self):
        self.coord.x = self.level_width // 2
        self.coord.y = tile_to_real(4)
        self.coord.x_map = self.level_width // 2
        self.coord.y_map = self.level_height - tile_to_real(4)

    def init_costume(self, ship_type: PlayerShipType):
        match ship_type:
            case PlayerShipType.SHIP1:
                self.set_costume(self.costumes["ship_1"])
            case PlayerShipType.SHIP2:
                self.set_costume(self.costumes["ship_2"])
            case PlayerShipType.SHIP3:
                self.set_costume(self.costumes["ship_3_1"])
    
    def switch_to_blink_costume(self, ship_type: PlayerShipType):
        match ship_type:
            case PlayerShipType.SHIP1:
                self.set_costume(self.costumes["blink_ship_1"])
            case PlayerShipType.SHIP2:
                self.set_costume(self.costumes["blink_ship_2"])
            case PlayerShipType.SHIP3:
                self.set_costume(self.costumes["blink_ship_3"])

    def ship3_costume_set(self):
        if self.ship3_costume_idx:
            self.set_costume(self.costumes["ship_3_1"])
        else:
            self.set_costume(self.costumes["ship_3_2"])

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

    def player_tilemap_checker(self):
        """
        Get the current tilemap U,V and then fire events based on the tilemap (`minerals_check` or `check_level_complete`).
        """

        # ↓ These tiles are the _actual_ tile coordinates from the entire tilemap (not the map coordinates!).
        tile_x = real_to_tile(self.coord.x_map) + self.level.levelmap.map_x + 1
        tile_y = real_to_tile(self.coord.y_map) + self.level.levelmap.map_y + 1 + MAP_Y_OFFSET_TILES

        tilemap = pyxel.tilemap(0).pget(tile_x, tile_y)
        self.game.game_components.event_handler.trigger_event(events.TilemapPlayerCheck(tilemap, tile_x, tile_y))

    def move(self):
        self.player_tilemap_checker()

        self.coord.x_map += self.x_vel
        self.coord.y_map += self.y_vel
        self.x_vel -= self.drag * self.x_vel
        self.y_vel -= self.drag * self.y_vel

        if self.coord.x_map < 0:
            self.coord.x_map = 0
        elif self.coord.x_map > self.level_width - self.w:
            self.coord.x_map = self.level_width - self.w
        else:
            self.game.game_components.event_handler.trigger_event(events.StarsScroll)
            
        if self.coord.y_map > self.level_height - self.h:
            self.coord.y_map = self.level_height - self.h
        elif self.coord.y_map < 0:
            self.coord.y_map = 0
        else:
            self.game.game_components.event_handler.trigger_event(events.StarsScroll)

    def cam_update(self):
        self.game.game_components.camera.y = self.coord.y_map

        if self.game.game_components.camera.y > self.level_height - WINDOW_HEIGHT // 2:
            self.game.game_components.camera.y = self.level_height - WINDOW_HEIGHT // 2
            self.game.game_components.camera.dir_y = 0
        elif self.game.game_components.camera.y < WINDOW_HEIGHT // 2:
            self.game.game_components.camera.y = WINDOW_HEIGHT // 2
            self.game.game_components.camera.dir_y = 0
        else:
            self.game.game_components.camera.dir_y = self.y_vel
            self.game.game_components.camera.dir_x = self.x_vel
        
    def update(self):
        self.map_to_view(self.game.game_components.camera.y)
        self.cam_update()

        self.move()

        self.update_speed_statusbar()

        self.update_if_has_been_hit()

        self.game.game_components.event_handler.trigger_event(events.FlameUpdate(self.coord.x, self.coord.y, self.h))
            
        if self.level.idx == 3:
            if self.ship3_costume_ticker.get() and not self.has_been_hit:
                self.ship3_costume_idx = not self.ship3_costume_idx
                self.ship3_costume_set()

    def update_if_has_been_hit(self):
        if self.has_been_hit:
            if self.blinking_ticker.get():
                self.hit_blink_count += 1
                self.hit_blink_idx = not self.hit_blink_idx
            self.draw_if_hit()

    def update_speed_statusbar(self):
        if self.speed_statusbar_ticker.get():
            self.game.game_components.event_handler.trigger_event(events.UpdateStatusbar)

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

        pyxel.blt(self.coord.x, self.coord.y, self.img, self.u, self.v, self.w, self.h, self.colkey)

    def level_reset(self):
        self.player_setup()

    # Event handler functions
    
    def is_colliding_with_enemy(self, enemy_x: float, enemy_y: float, enemy_w: int, enemy_h: int) -> bool:
        if self.is_colliding(enemy_x, enemy_y, enemy_w, enemy_h):
            if not self.has_been_hit:
                self.game.game_components.event_handler.trigger_event(events.PlayerHealthChange(-1))
                self.health -= 1
                self.has_been_hit = True
                self.game.game_components.soundplayer.play(self.soundbank["attacked"])
            if self.health == 0:
                self.game.game_components.event_handler.trigger_event(events.LevelRestart)
                return True
        return False

    def restart_handler(self):
        self.coord.x_map = self.level_width // 2
        self.coord.y_map = self.level_height - tile_to_real(4)
        self.x_vel = 0
        self.y_vel = 0
        self.game.game_components.event_handler.trigger_event(events.PlayerHealthChange(self.level.max_health))
        self.health = self.level.max_health

  
class PlayerHandler(SpriteHandler):

    def __init__(self, game_handler: GameHandler):
        self.game_handler = game_handler
        self.game_handler.game_components.event_handler.add_handler(events.ActivateLevel.name, lambda: self._tweak_player_keys_state(True))
        self.player = Player(self.game_handler)
        self.setup()

        self.soundbank = {
            "shoot": Sfx(SoundType.AUDIO, 0, 10),
        }
        self.keybindings = {
            "player_right": KeyFunc([pyxel.KEY_RIGHT, pyxel.KEY_D], lambda: self.player.move_handler(Direction.RIGHT), active=False),
            "player_left": KeyFunc([pyxel.KEY_LEFT, pyxel.KEY_A], lambda: self.player.move_handler(Direction.LEFT), active=False),
            "player_up": KeyFunc([pyxel.KEY_UP, pyxel.KEY_W], lambda: self.player.move_handler(Direction.UP), active=False),
            "player_down": KeyFunc([pyxel.KEY_DOWN, pyxel.KEY_S], lambda: self.player.move_handler(Direction.DOWN), active=False),
            "player_shoot": KeyFunc([pyxel.KEY_SPACE], self.shoot_handler, KeyTypes.BTNP, hold_time=10, repeat_time=10, active=False),
        }
        self.statusbar_items = [
            TextStatusbarItem(100, self.get_player_speed, pyxel.COLOR_YELLOW),
        ]

    def _tweak_player_keys_state(self, state: bool):
        for key in self.keybindings.values():
            key.active = state

    def setup(self):
        self._tweak_player_keys_state(False)
        level = self.game_handler.levelhandler.get_curr_lvl()

        if level.idx == 3:
            self.has_flame = False
        else:
            self.flame = Flame(self.game_handler)
            self.has_flame = True

    def draw(self):
        if self.has_flame:
            self.flame.draw()

        self.player.draw()

    def update(self):
        if self.has_flame:
            self.flame.update()

        self.player.update()

    def init_level(self):
        self.setup()
        self.player.player_setup()

    def restart_level(self):
        self.player.restart_handler()
    
    def shoot_handler(self):
        self.game_handler.game_components.event_handler.trigger_event(events.PlayerShootBullets(self.player.coord.x_map, self.player.coord.y_map))
        self.game_handler.game_components.soundplayer.play(self.soundbank["shoot"])

    def enable_keybinds(self):
        for key in self.keybindings.values():
            key.active = True

    # Functions for statusbar
    def get_player_speed(self) -> str:

        magnitude = pyxel.floor(
            hypotenuse(self.player.y_vel, self.player.x_vel) * 100
        )
        return f"Kecepatan: {magnitude} km/h"