from ui import UI
from new_bci_framework.paradigm.paradigm import Paradigm
from new_bci_framework.paradigm.MI_paradigm import MIParadigm
from new_bci_framework.recorder.recorder import Recorder
from new_bci_framework.recorder.opeb_bci_cyton_recorder import CytonRecorder
from new_bci_framework.config.config import Config

import os
import time
import numpy as np

import pygame as pg
from pygame import Surface
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT


class OfflineUI(UI):
    def __init__(self, paradigm: Paradigm, recorder: Recorder, config: Config):
        super(OfflineUI, self).__init__(paradigm, recorder, config)

        self.recorder = recorder
        self.events = paradigm.get_events()

        # Initialize pygame
        pg.init()
        self.exit = False

        # UI params:
        ## Define constants for the screen width and height
        self.screen_width = 800
        self.screen_height = 600
        ## colors:
        self.bg_color = (248, 240, 227)
        ## font:
        pg.font.init()
        self.font = pg.font.SysFont('helvetica', 30)
        self.images = config.CLASSES_IMS

        # Create the screen object
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))

        # Start timing events
        self.time_between_trials = config.TIME_PER_TRIAL * 1_000
        self.timed_event_trial = pg.USEREVENT + 1
        pg.time.set_timer(self.timed_event_trial, self.time_between_trials)
        self.timed_event_wait = self.timed_event_trial + 1
        # run
        self.mainloop()

    def mainloop(self):
        while not self.exit and len(self.events) > 0:

            # Check for quiting events:
            for event in pg.event.get():
                if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
                    self.exit = True
                elif event.type == self.timed_event_trial:
                    marker = self.events[0]
                    self.events = self.events[1:]
                    image = pg.image.load(self.images[marker])
                    self.screen.blit(image, (self.screen_height / 2,
                                             self.screen_width / 2))
            # Fill the background with white
            # self.screen.fill(self.bg_color)

            # Flip the display
            pg.display.flip()

        # Done! Time to quit.
        pg.quit()

if __name__ == '__main__':
    config = Config()
    ui = OfflineUI(MIParadigm(config), Recorder(config), config)
