# Where to Start
The first thing you should read is the [\_\_main\_\_.py file](/misi_hijau/__main__.py). It contains the `App` class which is the class used to wrap the Pyxel `update` and `draw` functions.

# Player
The player is defined at [player.py](/misi_hijau/game/sprites/player.py).

# Entity Spawning
Enemies are stored as an array of coordinates in which the enemies should be spawn. The enemies will then be spawned accordingly based on the coordinate arrays. Since there are only one type of enemy in each level, the spawner doesn't need to check for the enemy type on every spawn.

Minerals and powerups are hardcoded in tilemaps. When the player touches them, the objects inside a tile will be replaced with black background.
