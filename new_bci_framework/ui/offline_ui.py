########################################################################################################################
#                                                      Imports                                                         #
########################################################################################################################
from new_bci_framework.ui.ui import UI
from new_bci_framework.config.config import Config

import pygame as pg
from time import sleep
from nptyping import NDArray


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

        self.add_images(config.CLASSES_IMS)

    def setup(self):
        pg.display.set_caption('Offline Session')
        super().setup()

    def display_event(self, label: str):
        sleep(self.config.TIME_BETWEEN_TRIALS)
        self.display_message(msg=label)
        self.display_image(self.images[label])
        sleep(self.config.TIME_PER_TRIAL)
        self.clear_screen()
