# Script to test behaviour of aliens

import pyxel

from game.sprites.enemy import EnemyGrug, EnemyPhong, EnemySquidge, EnemyEntity, EnemyType
from game.sprites.minerals import MineralType
from core.common import Level, LevelMap, PlayerShipType, TickerItem
from res.resources_load import PYXEL_RESOURCE_PATH

pyxel.init(256, 256, fps=30)
pyxel.load(PYXEL_RESOURCE_PATH)

dummy_level = Level(0, LevelMap(0, 0, 32, 32, []), PlayerShipType.SHIP_1, EnemyType.ENEMY_1, MineralType.MINERAL_1, 0, 0, 0, 0, 0)

ticker_1 = TickerItem(4)
ticker_2 = TickerItem(3)

camera_y = 0

class EnemyHandler:
    def __init__(self):
        self.enemies: list[EnemyEntity] = []
        self.add_testing_enemies()

    def add_testing_enemies(self):
        self.enemies.append(EnemyGrug(10, 128, dummy_level, ticker_1))
        self.enemies.append(EnemyPhong(30, 128, dummy_level, ticker_2))
        self.enemies.append(EnemySquidge(50, 128, dummy_level))

    def draw(self):
        for enemy in self.enemies:
            enemy.draw()

    def update(self):
        for enemy in self.enemies:
            enemy.update()

enemy_handler = EnemyHandler()

def game_draw_loop():
    pyxel.cls(0)
    enemy_handler.draw()

def game_update_loop():
    ticker_1.tick()
    ticker_2.tick()
    enemy_handler.update()

pyxel.run(game_update_loop, game_draw_loop)