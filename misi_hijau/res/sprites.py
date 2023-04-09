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

from game.sprites import Sprite, SpriteHandler, TilemapBasedSprite, player, minerals, enemy, flag, bullets, blasts, powerups
from game.game_handler import GameHandler

class SpritesFactory:
    """
    A sprite factory.
    """
    def __init__(self, game_handler: GameHandler):
        self.game_handler = game_handler

    def create_tilemap_sprites(self) -> dict[str, TilemapBasedSprite]:
        tilemap_sprites: dict[str, TilemapBasedSprite] = {
            "flag": flag.LevelFlag(self.game_handler),
            "minerals": minerals.MineralsHandler(self.game_handler),
            "powerups": powerups.PowerUpHandler(self.game_handler)
        }
        return tilemap_sprites
    
    def create_sprite_handlers(self) -> dict[str, SpriteHandler]:
        sprite_handlers: dict[str, SpriteHandler] = {
            "enemy": enemy.EnemyHandler(self.game_handler),
            "player": player.PlayerHandler(self.game_handler),
            "blasts": blasts.BlastsHandler(self.game_handler),
            "bullets": bullets.BulletsHandler(self.game_handler)
        }

        return sprite_handlers
    
    def create_raw_sprites(self) -> dict[str, Sprite]:
        raw_sprites: dict[str, Sprite] = {

        }
        return raw_sprites