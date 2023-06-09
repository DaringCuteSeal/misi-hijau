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
Common utilities.
"""

import math # don't use pyxel's sqrt beacuse it returns denormalized number (pyxel.sqrt(0) returns max possible value of int)
import pyxel
# Functions
def tile_to_real(size: int) -> int:
    """
    Get real size in pixel from a tilemap size.
    """
    return size * pyxel.TILE_SIZE

def real_to_tile(size: float) -> int:
    """
    Get tilemap size from real pixel size.
    """
    size = size // pyxel.TILE_SIZE
    return pyxel.floor(size)

def round_to_tile(size: float) -> int:
    """
    Round a number to closest multiple of TILE_SIZE.
    """
    return pyxel.ceil(size / pyxel.TILE_SIZE) * pyxel.TILE_SIZE

def hypotenuse(a: int | float, b: int | float) -> float:
    """
    Get the hypotenuse of a triangle, given that A and B are the sides.
    """
    return math.sqrt(a**2+b**2)

def reverse_hypotenuse(c: int | float, a: int | float) -> float:
    """
    Get one missing side of a triangle, given the hypotenuse and one other side.
    """
    return math.sqrt(c**2-a**2)