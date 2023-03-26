import pyxel


# Tick handling
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