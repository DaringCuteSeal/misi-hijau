# Copyright 2023 Cikitta Tjok <daringcuteseal@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pyxel

from game.game_handler import GameHandler
from game import events
from res.storyline_text import story_text

class StoryDialogs:
    DIALOG_WIDTH = 200

    def __init__(self, game_handler: GameHandler):
        self.event_handler = game_handler.game_components.event_handler
        self.event_handler.add_handler(events.StartGame.name, self.start_game_dialog)
    
    def start_game_dialog(self):
        self.event_handler.trigger_event(
            events.ShowDialog(
                story_text["story_start_level_1"][0],
                self.DIALOG_WIDTH,
                5,
                pyxel.COLOR_WHITE,
                pyxel.COLOR_ORANGE,
                None,
                pyxel.KEY_Q
            )
        )