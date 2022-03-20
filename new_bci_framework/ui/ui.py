########################################################################################################################
#                                                      Imports                                                         #
########################################################################################################################
from new_bci_framework.recorder.recorder import Recorder

import time
import numpy as np
import pygame as pg
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT

from typing import Tuple, Any
from nptyping import NDArray, Int8


########################################################################################################################
#                                                   Implementation                                                     #
########################################################################################################################
class UI:
    def __init__(self):
        # screen width and height:
        self.screen_width = 800
        self.screen_height = 600
        self.center = (self.screen_width / 2, self.screen_height / 2)

        # colors:
        self.bg_color = (248, 240, 227)
        self.bar_color = '#306DA3'

        # font:
        pg.font.init()
        self.font = pg.font.SysFont('Roboto', 50)

        # Progress bar:
        self.bar_w = 400
        self.bar_h = 20
        self.bar_x = self.screen_width / 2 - self.bar_w / 2
        self.bar_y = self.screen_height * 0.9 - self.bar_h / 2

        # Declare vars:
        self.to_exit = False
        self.first_iter = True
        self.event_start_time = 0

        self.screen = None
        self.events = None
        self.work = 0

    def run(self, recorder: Recorder, events: NDArray):
        self.events = np.copy(events)
        self.work = len(self.events)
        # Initialize pygame
        pg.init()
        self._setup()
        # run
        self.mainloop(recorder)
        # Done! Time to quit.
        self.__quit()

    def mainloop(self, recorder: Recorder):
        while not self.to_exit:
            self.single_iter_work(recorder)

    def single_iter_work(self, recorder: Recorder):
        raise NotImplemented

    def _setup(self):
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))

        self.screen.fill(self.bg_color)
        self._display_message('Hello, training session will start soon', self.center)
        time.sleep(2)

        self.screen.fill(self.bg_color)
        self._display_message('Starting now', self.center)
        time.sleep(1)

        self._clear_screen()
        time.sleep(1)

    def _display_message(self, msg: str, loc: Tuple[float, float]):
        text = self.font.render(msg, True, 'black')
        text_rect = text.get_rect(center=loc)
        self.screen.blit(text, text_rect)
        pg.display.flip()

    def _clear_screen(self):
        self.screen.fill(self.bg_color)
        self.__update_loading_bar()
        pg.display.flip()

    def _check_if_to_quit(self, event: int) -> None:
        self.to_exit = (event == KEYDOWN and event == K_ESCAPE) or event == QUIT

    def __update_loading_bar(self):
        # Border:
        pg.draw.rect(self.screen, self.bar_color, pg.Rect(self.bar_x, self.bar_y, self.bar_w, self.bar_h), 1)

        # Bar
        progress = 1 - len(self.events) / self.work
        pg.draw.rect(self.screen, self.bar_color, pg.Rect(self.bar_x, self.bar_y, self.bar_w * progress, self.bar_h))

    def __quit(self):
        self._clear_screen()
        self._display_message('Session is over, Thanks!', self.center)
        time.sleep(1)
        pg.quit()

