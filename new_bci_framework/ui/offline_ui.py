########################################################################################################################
#                                                      Imports                                                         #
########################################################################################################################
from new_bci_framework.ui.ui import UI
from new_bci_framework.config.config import Config
from new_bci_framework.recorder.recorder import Recorder

import numpy as np
import pygame as pg
from time import sleep


########################################################################################################################
#                                                     Constants                                                        #
########################################################################################################################
MS2S = 1_000


########################################################################################################################
#                                                   Implementation                                                     #
########################################################################################################################
class OfflineUI(UI):

    def __init__(self, config: Config):
        super().__init__(config)

        # Progress bar:
        self.bar_color = '#9b2226'
        self.bar_w = 400
        self.bar_h = 20
        self.bar_x = self.screen_width / 2 - self.bar_w / 2
        self.bar_y = self.screen_height * 0.9 - self.bar_h / 2

        # Arrows:
        self.add_images(config.CLASSES_IMS)

    def setup(self):
        pg.display.set_caption('Offline Session')
        super(OfflineUI, self).setup()

        self.display_message('Hello, training session will start soon', loc=self.center)
        sleep(self.config.PAUSE_LENGTH * 2)

        self.screen.fill(self.bg_color)
        self.display_message('Starting now', loc=self.center)

    def display_event(self, recorder: Recorder, label: str, surface: pg.Surface) -> None:
        sleep(self.config.PAUSE_LENGTH)
        super().display_event(recorder, label, surface)

    def clear_surface(self, surface: pg.Surface):
        self.update_progress_bar()
        super(OfflineUI, self).clear_surface(surface)

    def quit(self):
        self.set_curr_work(self.work)
        self.clear_surface(self.screen)
        sleep(self.config.PAUSE_LENGTH)
        self.display_message('Session is over, Thanks!', loc=self.center)
        sleep(self.config.PAUSE_LENGTH)
        super(OfflineUI, self).quit()

    def update_progress_bar(self):
        # Border:
        pg.draw.rect(self.screen, self.bar_color, pg.Rect(self.bar_x, self.bar_y, self.bar_w, self.bar_h), 1)

        # Bar
        if self.work == 0 or np.isnan(self.work):
            progress = 1
        else:
            progress = 1 - (self.work - self.curr_work) / self.work
        pg.draw.rect(self.screen, self.bar_color, pg.Rect(self.bar_x, self.bar_y, self.bar_w * progress, self.bar_h))

