########################################################################################################################
#                                                      Imports                                                         #
########################################################################################################################
from new_bci_framework.ui.ui import UI
from new_bci_framework.recorder.recorder import Recorder
from new_bci_framework.config.config import Config

import pygame as pg
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
        super().__init__()

        # Paradigm params:
        self.classes = config.CLASSES
        self.idle_label = config.IDLE_LABEL
        self.images = config.CLASSES_IMS

        # timing:
        self.trial_time = config.TIME_PER_TRIAL
        self.event_time = (config.TIME_PER_TRIAL + config.TIME_BETWEEN_TRIALS) * MS2S  # convert to ms
        self.timed_event_trial = pg.USEREVENT + 1

    def run(self, recorder: Recorder, events: NDArray):
        super().run(recorder, events)

    def mainloop(self, recorder: Recorder):
        super().mainloop(recorder)

    def single_iter_work(self, recorder: Recorder):
        # Check events in queue:
        for event in pg.event.get():
            self._check_if_to_quit(event.type)  # Check for quiting events:
            if event.type == self.timed_event_trial:  # Check for timed event (trials)
                self._push_event(recorder)

        self._push_first_event(recorder)

        self._end_event()

    def _setup(self):
        pg.display.set_caption('Offline Session')
        super()._setup()

    def _push_event(self, recorder: Recorder):
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
        self._display_message(msg, (self.screen_width / 2, self.screen_height / 4))
        pg.display.flip()

        # Start timing event
        self.event_start_time = pg.time.get_ticks()

    def _push_first_event(self, recorder: Recorder) -> None:
        if self.first_iter:
            self._push_event(recorder)
            # Start timer
            pg.time.set_timer(self.timed_event_trial, self.event_time)
            self.first_iter = False

    def _end_event(self) -> None:
        if self.event_start_time != 0:
            event_passed_time = (pg.time.get_ticks() - self.event_start_time) / MS2S  # convert to seconds
            if event_passed_time >= self.trial_time:
                self._handle_event_end()

    def _handle_event_end(self):
        # clear event:
        self._clear_screen()
        if len(self.events) == 0:
            self.to_exit = True
        self.event_start_time = 0

