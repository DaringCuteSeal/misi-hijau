from game.game_ui import healthbar, stars, dialog
from core.game_handler import GameHandler
from core.game_ui_classes import UIComponent

STARS_COUNT = 100

class UIComponentFactory:
    """
    A UI Component factory.
    """
    def __init__(self, game_handler: GameHandler):
        self.game_handler = game_handler

    def create_ui_components(self) -> dict[str, UIComponent]:
        ui_components: dict[str, UIComponent] = {
            "healthbar": healthbar.HealthBar(self.game_handler),
            "dialog": dialog.Dialog(self.game_handler)
        }
        return ui_components
    
    def create_stars(self) -> stars.Stars:
        return stars.Stars(STARS_COUNT, self.game_handler)