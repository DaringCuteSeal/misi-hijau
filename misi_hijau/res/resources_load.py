import pyxel
import os

def load_resources():
    pyxel.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "res.pyxres"))
    pyxel.image(1).load(0, 0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "game_splash_screen.png"))