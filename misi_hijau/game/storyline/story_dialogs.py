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
import os

from core.common import WINDOW_WIDTH, WINDOW_HEIGHT, KeyFunc, KeyType
from core.game_handler import GameHandler
from game import events

from res.storyline_text import story_text
from res.resources_load import LEVEL_STATS_IMAGE_PATH, TEMP_IMG_BANK_IDX

class InGameStoryline:

    DIALOG_WIDTH = 200

    def __init__(self, game_handler: GameHandler):
        self.game_handler = game_handler
        self.level_handler = game_handler.levelhandler
        self.event_handler = game_handler.game_components.event_handler
        self.timer = game_handler.game_components.timer
        self.init_event_handlers()
        self.setup_level_stats_keyfunc()

    def setup_level_stats_keyfunc(self):
        self.close_stats_keyfunc = KeyFunc([pyxel.KEY_SPACE], self.close_level_stats, KeyType.BTN, active=False)
        self.game_handler.game_components.keylistener.add("close_stats_keyfunc", self.close_stats_keyfunc)
    
    def init_event_handlers(self):
        # Dialog
        self.event_handler.add_handler(events.StartGame.name, self.show_dialog_handler)
        self.event_handler.add_handler(events.ShowLevelDialog.name, self.show_dialog_handler)
        self.event_handler.add_handler(events.LevelRestart.name, self._show_level_restart_dialog)

        # Level stats
        self.event_handler.add_handler(events.ShowLevelStats.name, self.show_level_stats_handler)
        self.event_handler.add_handler(events.BroadcastEnemiesCount.name, self.save_enemies_count)

    ##########
    # Dialog #
    ##########

    dialog_strings: list[str] = [
        story_text["story_start_level_1"][0],
        story_text["story_start_level_2"][0],
        story_text["story_start_level_3"][0]
    ]

    def show_dialog_handler(self):
        curr_level_idx = self.level_handler.get_curr_lvl().idx - 1
        self._show_dialog_by_level_idx(curr_level_idx)

    def _show_dialog_by_level_idx(self, level_idx: int):
        self.event_handler.trigger_event(
            events.ShowDialog(
                self.dialog_strings[level_idx],
                self.DIALOG_WIDTH,
                pyxel.COLOR_WHITE,
                pyxel.COLOR_BROWN,
                5,
                lambda: self.event_handler.trigger_event(events.ActivateLevel),
                pyxel.KEY_Q,
                sfx=True,
                show_dismiss_msg=True,
                dismiss_msg_col= pyxel.COLOR_YELLOW,
                dismiss_msg_str="q untuk abaikan dan mulai.."
            )
        )
    
    def _show_level_restart_dialog(self):
        self.event_handler.trigger_event(
            events.ShowDialog(
                "Pesawat ruang angkasamu hancur, levelmu telah diulang!",
                self.DIALOG_WIDTH,
                pyxel.COLOR_WHITE,
                pyxel.COLOR_NAVY,
                5,
                lambda: self.event_handler.trigger_event(events.ActivateLevel),
                pyxel.KEY_Q,
                sfx=False,
                show_dismiss_msg=True,
                dismiss_msg_col=pyxel.COLOR_YELLOW,
                dismiss_msg_str="q untuk abaikan dan mulai kembali..",
            )
        )
    
    ###############
    # Level stats #
    ###############

    HINT_TEXT_STRING = "tekan spasi untuk lanjut..."
    HINT_TEXT_COORD = (5, WINDOW_HEIGHT - pyxel.FONT_HEIGHT - 5)

    STATS_TEXT_COL = pyxel.COLOR_WHITE
    ENEMIES_STATS_COORD = (35, 124)
    MINERALS_STATS_COORD = (152, 124)

    def show_level_stats_handler(self):
        self._disable_callable_draw()

        curr_level_idx = self.level_handler.get_curr_lvl().idx
        self.timer.attach(2).when_over(lambda: self.alter_keylistener_state(True))
        self.timer.attach(2).when_over(self._show_blinking_text_hint)
        self._load_draw_level_stats_background(curr_level_idx)
        self._get_minerals_count()
        self._draw_stats_text()

    def _disable_callable_draw(self):
        self.game_handler.game_components.event_handler.trigger_event(events.StopGameLoop)

    def _show_blinking_text_hint(self):
        self.event_handler.trigger_event(events.ShowBlinkingTextHint(self.HINT_TEXT_COORD[0], self.HINT_TEXT_COORD[1], self.HINT_TEXT_STRING, pyxel.COLOR_WHITE, TEMP_IMG_BANK_IDX, False))

    def alter_keylistener_state(self, state: bool):
        self.close_stats_keyfunc.active = state

    def _draw_stats_text(self):
        pyxel.text(self.ENEMIES_STATS_COORD[0], self.ENEMIES_STATS_COORD[1], self._get_enemies_stats_str(), self.STATS_TEXT_COL) # enemies
        pyxel.text(self.MINERALS_STATS_COORD[0], self.MINERALS_STATS_COORD[1], self._get_minerals_stats_str(), self.STATS_TEXT_COL) # minerals
    
    def _get_minerals_count(self):
        # The amount of minerals is accessible through the game's level.
        level = self.level_handler.get_curr_lvl()
        self.minerals_count = level.minerals_count
    
    def save_enemies_count(self, count: int):
        # The amount of enemies is NOT accessible through the game's level, so
        # we save the amount of enemies through an event broadcasted by the
        # enemies handler when it counts the amount of enemies in a level.
        self.enemies_count = count

    def _get_enemies_stats_str(self) -> str:
        return f"Kamu memusnahkan\n   {self.enemies_count:>3} alien" # lazy to do the math ^_^
    
    def _get_minerals_stats_str(self) -> str:
        return f"Kamu mengumpulkan\n  {self.minerals_count:>3} mineral" # still lazy to do the math ^w^

    def close_level_stats(self):
        self.event_handler.trigger_event(events.HideBlinkingTextHint)
        self.event_handler.trigger_event(events.LevelNext)
        self.game_handler.game_components.event_handler.trigger_event(events.ResumeGameLoop)
        self.alter_keylistener_state(False)

    def _load_draw_level_stats_background(self, idx: int):
        pyxel.image(TEMP_IMG_BANK_IDX).load(0, 0, os.path.join(LEVEL_STATS_IMAGE_PATH, f"{idx}.png"))
        pyxel.blt(0, 0, TEMP_IMG_BANK_IDX, 0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)