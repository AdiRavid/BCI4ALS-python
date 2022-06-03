########################################################################################################################
#                                                      Imports                                                         #
########################################################################################################################
import numpy as np

from new_bci_framework.config.config import Config
from new_bci_framework.recorder.recorder import Recorder

from time import sleep
import pygame as pg
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT

from typing import Tuple, Optional, Dict

BLACK = (0, 0, 0)
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

        self.msg_surface = pg.Surface((self.screen_width - 100, self.screen_height - 100))

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
        pg.init()
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        self.screen.fill(self.bg_color)

    def display_event(self, recorder: Recorder, label: str, surface: pg.Surface) -> None:

        self.display_message(msg=f'READY? Think {label}')
        self.display_image(self.images[label])
        sleep(self.config.PRE_CUE_LENGTH)

        recorder.push_marker(self.config.TRIAL_LABELS[label])

        self.clear_surface(surface)
        self.display_image(self.images[label])
        sleep(self.config.CUE_LENGTH)
        self.clear_surface(surface)

    def ready(self, label: str):
        self.display_message(msg=f'READY? Think {label}')
        self.display_image(self.images[label])
        sleep(self.config.PRE_CUE_LENGTH)

    def display_message(self, msg: str, size: int = 50, loc: Optional[Tuple[float, float]] = None, color=BLACK):
        font = pg.font.SysFont(name='Roboto', size=size)

        text = font.render(msg, True, color)
        text_rect = text.get_rect(center=self.msg_loc if loc is None else loc)
        self.screen.blit(text, text_rect)

        pg.display.flip()

    def display_image(self, image: pg.image):
        image_rect = image.get_rect(center=self.img_loc)
        self.screen.blit(image, image_rect)
        pg.display.flip()

    def clear_surface(self, surface: pg.Surface):
        surface.fill(self.bg_color)
        self.screen.blit(surface, (50, 50))
        pg.display.flip()

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

    def display_prediction(self, label, prediction):
        raise NotImplementedError

    @staticmethod
    def need_to_quit() -> bool:
        for event in pg.event.get():
            if (event == KEYDOWN and event == K_ESCAPE) or event.type == QUIT:
                return True
        return False
