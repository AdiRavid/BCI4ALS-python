from new_bci_framework.ui.ui import UI
from new_bci_framework.recorder.recorder import Recorder
from new_bci_framework.config.config import Config

import time
import numpy as np
from typing import Tuple
from nptyping import NDArray

import pygame as pg
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT


MS2S = 1_000


class OfflineUI(UI):
    def __init__(self, config: Config):
        super(OfflineUI, self).__init__(config)

        # Paradigm params:
        self.classes = config.CLASSES
        self.idle_label = config.IDLE_LABEL
        # timing:
        self.trial_time = config.TIME_PER_TRIAL
        self.event_time = (config.TIME_PER_TRIAL + config.TIME_BETWEEN_TRIALS) * MS2S  # convert to ms
        self.timed_event_trial = pg.USEREVENT + 1

        # UI params:
        ## screen width and height:
        self.screen_width = 800
        self.screen_height = 600
        self.center = (self.screen_width / 2, self.screen_height / 2)
        ## colors:
        self.bg_color = (248, 240, 227)
        self.bar_color = '#306DA3'
        ## font:
        pg.font.init()
        self.font = pg.font.SysFont('Roboto', 50)
        ## images:
        self.images = config.CLASSES_IMS

        # Progress bar:
        self.bar_w = 400
        self.bar_h = 20
        self.bar_x = self.screen_width / 2 - self.bar_w / 2
        self.bar_y = self.screen_height * 0.9 - self.bar_h / 2

        # Declare unknown vars:
        self.screen = None
        self.events = None
        self.work = 0

    def run(self, recorder: Recorder, events: NDArray):
        self.events = np.copy(events)
        self.work = len(self.events)
        # Initialize pygame
        pg.init()
        self.__setup(recorder)
        # run
        self.__mainloop(recorder)

    def __setup(self, recorder: Recorder):

        pg.display.set_caption('Offline Training Session')
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))

        self.screen.fill(self.bg_color)
        self.__display_message('Hello, training session will start soon', self.center)
        time.sleep(2)

        self.screen.fill(self.bg_color)
        self.__display_message('Starting now', self.center)
        time.sleep(1)

    def __display_message(self, msg: str, loc: Tuple[float, float]):
        text = self.font.render(msg, True, 'black')
        text_rect = text.get_rect(center=loc)
        self.screen.blit(text, text_rect)
        pg.display.flip()

    def __mainloop(self, recorder):
        # CLear screen
        self.__clear_screen()
        time.sleep(1)

        # Start loop
        to_exit = False
        first_iter = True
        event_start_time = 0
        while not to_exit:
            for event in pg.event.get():
                # Check for quiting events:
                if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
                    to_exit = True
                # Check for timed event
                elif event.type == self.timed_event_trial:
                    self.__push_event(recorder)
                    event_start_time = pg.time.get_ticks()

            if first_iter:
                # Start timer
                self.__push_event(recorder)
                event_start_time = pg.time.get_ticks()
                pg.time.set_timer(self.timed_event_trial, self.event_time)
                first_iter = False

            if event_start_time != 0:
                event_passed_time = (pg.time.get_ticks() - event_start_time) / MS2S  # convert to seconds
                if event_passed_time >= self.trial_time:
                    self.__clear_screen()
                    if len(self.events) == 0:
                        to_exit = True
                    event_start_time = 0

        # Done! Time to quit.
        self.__quit(recorder)

    def __clear_screen(self):
        self.screen.fill(self.bg_color)
        self.__update_loading_bar()
        pg.display.flip()

    def __update_loading_bar(self):
        # Border:
        pg.draw.rect(self.screen, self.bar_color, pg.Rect(self.bar_x, self.bar_y, self.bar_w, self.bar_h), 1)

        # Bar
        progress = 1 - len(self.events) / self.work
        pg.draw.rect(self.screen, self.bar_color, pg.Rect(self.bar_x, self.bar_y, self.bar_w * progress, self.bar_h))

    def __push_event(self, recorder: Recorder):
        # Pop event:
        event = self.events[0]
        self.events = self.events[1:]

        # Record event
        recorder.push_marker(event)

        # Display
        image = pg.image.load(self.images[event])
        image_rect = image.get_rect(center=(self.screen_width / 2, self.screen_height / 2))
        self.screen.blit(image, image_rect)

        label = self.classes[event]
        msg = f'Think {label}' if label != self.idle_label else ''
        self.__display_message(msg, (self.screen_width / 2, self.screen_height / 4))

        pg.display.flip()
        return

    def __quit(self, recorder: Recorder):
        self.__clear_screen()
        self.__display_message('Session is over, Thanks!', self.center)
        time.sleep(1)
        pg.quit()

