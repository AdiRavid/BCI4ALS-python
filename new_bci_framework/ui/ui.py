########################################################################################################################
#                                                      Imports                                                         #
########################################################################################################################
import numpy as np

from new_bci_framework.config.config import Config

import time
import pygame as pg
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT

from typing import Tuple, Optional, Dict


########################################################################################################################
#                                                   Implementation                                                     #
########################################################################################################################
class UI:
    def __init__(self, config: Config):
        self.config = config

        # screen width and height:
        self.screen_width = 800
        self.screen_height = 600
        self.center = (self.screen_width / 2, self.screen_height / 2)
        self.msg_loc = self.screen_width / 2, self.screen_height / 4
        self.screen = None

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

        # To be added after init
        self.work: int = np.nan
        self.images: Dict[str, pg.image] = {}

    def setup(self):
        pg.init()

        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))

        self.screen.fill(self.bg_color)
        self.display_message('Hello, training session will start soon', self.center)
        time.sleep(2)

        self.screen.fill(self.bg_color)
        self.display_message('Starting now', self.center)
        time.sleep(1)

    def display_event(self, label: str) -> None:
        raise NotImplemented

    def set_work(self, work):
        self.work = work

    def add_images(self, images: Dict[str, str]):
        images = {label: pg.image.load(img) for label, img in images.items()}
        self.images = {**self.images, **images}

    def display_message(self, msg: str, loc: Optional[Tuple[float, float]] = None):
        text = self.font.render(msg, True, 'black')
        loc = self.msg_loc if loc is None else loc
        text_rect = text.get_rect(center=loc)
        self.screen.blit(text, text_rect)
        pg.display.flip()

    def display_image(self, image: pg.image):
        image_rect = image.get_rect(center=self.center)
        self.screen.blit(image, image_rect)
        pg.display.flip()

    def update_progress_bar(self, work_remained=0):
        # Border:
        pg.draw.rect(self.screen, self.bar_color, pg.Rect(self.bar_x, self.bar_y, self.bar_w, self.bar_h), 1)

        # Bar
        if self.work == 0 or np.isnan(self.work):
            progress = 1
        else:
            progress = 1 - work_remained / self.work
        pg.draw.rect(self.screen, self.bar_color, pg.Rect(self.bar_x, self.bar_y, self.bar_w * progress, self.bar_h))

        pg.display.flip()

    def clear_screen(self):
        self.screen.fill(self.bg_color)
        pg.display.flip()

    def quit(self):
        self.clear_screen()
        self.display_message('Session is over, Thanks!', self.center)
        time.sleep(1)
        pg.quit()

    @staticmethod
    def need_to_quit() -> bool:
        for event in pg.event.get():
            if (event == KEYDOWN and event == K_ESCAPE) or event == QUIT:
                return True
        return False
