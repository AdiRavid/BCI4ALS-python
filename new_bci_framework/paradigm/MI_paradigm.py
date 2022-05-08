from new_bci_framework.paradigm.paradigm import Paradigm
from new_bci_framework.config.config import Config
from new_bci_framework.ui.ui import UI
from new_bci_framework.recorder.recorder import Recorder

import numpy as np
import pygame as pg
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT


class MIParadigm(Paradigm):
    """
    Paradigm subclass for the motor-imagery paradigm.
    """

    def __init__(self, config: Config, ui: UI):
        super(MIParadigm, self).__init__(config)
        self.trial_labels = config.TRIAL_LABELS
        self.num_trials_per_class = config.NUM_TRIALS_PER_CLASS

        self.events = self.__get_event_list()
        self.work = len(self.events)

        self.ui = ui

    def start(self, recorder: Recorder):
        self.ui.setup()
        self.ui.set_work(len(self.events))

        for i in range(self.work):
            if self.ui.need_to_quit():
                break
            self.ui.set_curr_work(i)
            self.ui.clear_screen()
            self.ui.display_event(recorder, self.events[i])
        self.ui.quit()

    def __get_event_list(self):
        events = np.hstack([np.full(self.num_trials_per_class, key) for key in self.trial_labels.keys()])
        np.random.default_rng().shuffle(events)
        return events

