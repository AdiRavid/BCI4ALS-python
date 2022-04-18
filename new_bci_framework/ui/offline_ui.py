########################################################################################################################
#                                                      Imports                                                         #
########################################################################################################################
from new_bci_framework.ui.ui import UI
from new_bci_framework.config.config import Config
from new_bci_framework.recorder.recorder import Recorder

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

    def display_event(self, recorder: Recorder, label: str):
        sleep(self.config.PAUSE_LENGTH)

        self.display_message(msg=f'READY? Think {label}')
        self.display_image(self.images[label])
        sleep(self.config.PRE_CUE_LENGTH)

        recorder.push_marker(self.config.TRIAL_LABELS[label])

        self.clear_screen()
        self.display_image(self.images[label])
        sleep(self.config.CUE_LENGTH)
        self.clear_screen()
