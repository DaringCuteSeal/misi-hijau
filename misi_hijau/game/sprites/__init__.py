import pyxel

from .. import base
from dataclasses import dataclass, field

@dataclass
class Sprite:
    """
    A sprite class with some predefined functions to make costume handling easier.
    """
    coord: base.Coordinate
    img: int = 0
    u: int = 0
    v: int = 0
    w: int = 8
    h: int = 8
    speed: int = 1
    colkey: int | None = None
    costume_i: int = 0
    costumes: dict[str, tuple[int, int]] = field(default_factory=base.default_costumes)

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

