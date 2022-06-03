from mne.io import read_raw_fif

from new_bci_framework.session.session import Session
from new_bci_framework.config.config import Config
from new_bci_framework.recorder.recorder import Recorder
from new_bci_framework.ui.ui import UI
from new_bci_framework.paradigm.paradigm import Paradigm
from new_bci_framework.preprocessing.preprocessing_pipeline import PreprocessingPipeline
from new_bci_framework.classifier.base_classifier import BaseClassifier

import numpy as np
from sklearn.model_selection import train_test_split


class OfflineSession(Session):
    """
    Subclass of session for an offline recording session.
    """

    def __init__(self, config: Config, recorder: Recorder, ui: UI, paradigm: Paradigm,
                 preprocessor: PreprocessingPipeline, classifier: BaseClassifier):
        super().__init__(config, recorder, ui, paradigm, preprocessor, classifier)
        self.save = True

    def run_paradigm(self):
        events = self.paradigm.get_events()
        work = len(events)
        self.ui.set_work(work)

        self.ui.setup()
        for i in range(work):
            if self.ui.need_to_quit():
                break
            self.ui.set_curr_work(i)
            self.ui.clear_surface(self.ui.screen)
            self.ui.display_event(self.recorder, events[i], self.ui.screen)
        self.ui.quit()

    def run_classifier(self, split=True):
        if split:
            X_train, X_test, y_train, y_test = train_test_split(self.processed_data, self.labels)
        else:
            X_train, y_train = self.processed_data, self.labels
        self.classifier.fit(X_train, y_train)

    def run_evaluation(self):
        X_test, y_test = self.processed_data, self.labels
        self.classifier.evaluate(X_test, y_test)

    def run_all_without_classifier(self, raw_data_path=''):
        if not raw_data_path:
            self.run_recording()
            self.raw_data = self.recorder.get_raw_data()
        else:
            self.raw_data = read_raw_fif(raw_data_path, preload=True)

        self.filename = self.raw_data.filenames[0].split('/')[-1].split('.')[0]
        self.run_preprocessing()
        # self.feature_selection()
        self.run_evaluation()

    # if given raw_data it will do the pipeline on it
    # if no data were given it will evoke the recorder

    def run_all(self, raw_data_path=''):
        if not raw_data_path:
            self.run_recording()
            self.raw_data = self.recorder.get_raw_data()
        else:
            self.raw_data = read_raw_fif(raw_data_path, preload=True)

        self.filename = self.raw_data.filenames[0].split('/')[-1].split('.')[0]
        self.run_preprocessing()
        # self.feature_selection()
        self.run_classifier(split=False)  # TODO: change split
