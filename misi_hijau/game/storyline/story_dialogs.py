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

from core.game_handler import GameHandler
from game import events
from res.storyline_text import story_text

class StoryDialogs:
    DIALOG_WIDTH = 200

    dialog_strings: list[str] = [
        story_text["story_start_level_1"][0],
        story_text["story_start_level_2"][0],
        story_text["story_start_level_3"][0]
    ]

    def __init__(self, game_handler: GameHandler):
        self.level_handler = game_handler.levelhandler
        self.event_handler = game_handler.game_components.event_handler
        self.event_handler.add_handler(events.StartGame.name, self.show_dialog_handler)
        self.event_handler.add_handler(events.LevelNext.name, self.show_dialog_handler)
    
    def show_dialog_handler(self):
        curr_level_idx = self.level_handler.get_curr_lvl().idx - 1
        self._show_dialog_by_level_idx(curr_level_idx)

    def _show_dialog_by_level_idx(self, level_idx: int):
        self.event_handler.trigger_event(
            events.ShowDialog(
                self.dialog_strings[level_idx],
                self.DIALOG_WIDTH,
                5,
                pyxel.COLOR_WHITE,
                pyxel.COLOR_BROWN,
                lambda: self.event_handler.trigger_event(events.ActivateLevel),
                pyxel.KEY_Q,
                True,
                show_dismiss_msg=True,
                dismiss_msg_col= pyxel.COLOR_YELLOW,
                dismiss_msg_str="q untuk abaikan dan mulai.."
            )
        )
 