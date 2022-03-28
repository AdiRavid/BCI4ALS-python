from new_bci_framework.paradigm.paradigm import Paradigm
from new_bci_framework.config.config import Config
from new_bci_framework.ui.ui import UI
from new_bci_framework.recorder.recorder import Recorder

import numpy as np
from time import sleep


class MIParadigm(Paradigm):
    """
    Paradigm subclass for the motor-imagery paradigm.
    """

    def __init__(self, config: Config, ui: UI):
        super(MIParadigm, self).__init__(config)
        self.class_map = config.CLASSES_MAP

        self.num_trials_per_class = config.NUM_TRIALS_PER_CLASS
        self.time_per_trial = config.TIME_PER_TRIAL
        self.time_between_trials = config.TIME_BETWEEN_TRIALS

        self.events = self.__get_event_list()
        self.work = len(self.events)

        self.ui = ui

    def start(self, recorder: Recorder):
        self.ui.setup()
        self.ui.set_work(len(self.events))

        for i in range(self.work):
            self.ui.clear_screen()
            self.ui.update_progress_bar(work_remained=self.work - i)
            if self.ui.need_to_quit():
                break
            self.ui.display_event(self.events[i])
        self.ui.quit()

    def __get_event_list(self):
        events = np.hstack([np.full(self.num_trials_per_class, key) for key in self.class_map.keys()])
        np.random.default_rng().shuffle(events)
        return events

