########################################################################################################################
#                                                      Imports                                                         #
########################################################################################################################
import numpy as np

from new_bci_framework.config.config import Config
from new_bci_framework.recorder.recorder import Recorder

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
        self.img_loc = self.center
        self.screen = None

        # colors:
        self.bg_color = (248, 240, 227)

        # font:
        pg.font.init()
        self.font = pg.font.SysFont('Roboto', 50)

        # To be added after init:
        self.work: int = np.nan
        self.curr_work: int = 0
        self.images: Dict[str, pg.image] = {}

    def setup(self):
        raise NotImplemented

    def display_event(self, recorder: Recorder, label: str) -> None:
        raise NotImplemented

    def display_message(self, msg: str, loc: Optional[Tuple[float, float]] = None):
        text = self.font.render(msg, True, 'black')
        loc = self.msg_loc if loc is None else loc
        text_rect = text.get_rect(center=loc)
        self.screen.blit(text, text_rect)
        pg.display.flip()

    def display_image(self, image: pg.image):
        image_rect = image.get_rect(center=self.img_loc)
        self.screen.blit(image, image_rect)
        pg.display.flip()

    def clear_screen(self):
        raise NotImplemented

    def quit(self):
        pg.display.quit()
        pg.quit()

    def set_work(self, work):
        self.work = work

    def set_curr_work(self, curr_work):
        self.curr_work = curr_work

    def add_images(self, images: Dict[str, str]):
        images = {label: pg.image.load(img) for label, img in images.items()}
        self.images = {**self.images, **images}

    @staticmethod
    def need_to_quit() -> bool:
        for event in pg.event.get():
            if (event == KEYDOWN and event == K_ESCAPE) or event.type == QUIT:
                return True
        return False
