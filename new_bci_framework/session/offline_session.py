from new_bci_framework.session.session import Session
from new_bci_framework.config.config import Config
from new_bci_framework.recorder.recorder import Recorder
from new_bci_framework.ui.ui import UI
from new_bci_framework.paradigm.paradigm import Paradigm
from new_bci_framework.preprocessing.preprocessing_pipeline import PreprocessingPipeline
from new_bci_framework.classifier.base_classifier import BaseClassifier

import numpy as np
import pickle

from mne.io import read_raw_fif
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, mutual_info_classif


class OfflineSession(Session):
    """
    Subclass of session for an offline recording session.
    """

    def __init__(self, config: Config, recorder: Recorder, ui: UI, paradigm: Paradigm,
                 preprocessor: PreprocessingPipeline, classifier: BaseClassifier):
        super().__init__(config, recorder, ui, paradigm, preprocessor, classifier)
        self.save = True

    def run_recording(self):
        self.recorder.start_recording()
        self.recorder.plot_live_data()
        self.run_paradigm()
        self.recorder.end_recording()

        if self.save:
            self.raw_data = self.recorder.get_raw_data()
            self.raw_data.save(f'new_bci_framework/../data/{self.config.SUBJECT_NAME}_{self.config.DATE}_raw.fif')

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

    def run_preprocessing(self):
        self.epoched_data, self.epoched_labels = self.preprocessor.run_pipeline(self.raw_data)
        # self.preprocessor.run_pipeline(self.raw_data)

    # chose features
    # data is of size (n_epochs, n_features)
    # labels is of size n_epochs
    def feature_selection(self):
        num_of_features = self.config.NUM_OF_FEATURES

        X = self.epoched_data
        y = self.epoched_labels.ravel()
        if not self.config.SELECTED_FEATURES_PATH:
            selector = SelectKBest(score_func=mutual_info_classif, k=num_of_features)
            selector.fit(X, y)
            current_features_idxes = selector.get_support(indices=True)
            self.data_in_features = selector.fit_transform(X, y)
            pickle.dump(current_features_idxes, open("feature_selection", 'wb'))
        else:
            current_features_idxes = pickle.load(open(self.config.SELECTED_FEATURES_PATH, 'rb'))
            self.data_in_features = X[:, current_features_idxes]

        # self.data_in_features = SelectKBest(score_func=mutual_info_classif, k=num_of_features).fit_transform(X, y)

        # self.data_in_features = SelectKBest(score_func=f_classif, k=num_of_features).fit_transform(X, y)
        # self.data_in_features = SelectKBest(score_func=chi2, k=num_of_features).fit_transform(X, y) - cant use due to negative values
        # self.data_in_features = SelectKBest(score_func=f_regression, k=num_of_features).fit_transform(X, y)
        # self.data_in_features = SelectKBest(score_func=mutual_info_regression, k=num_of_features).fit_transform(X, y)

    def run_classifier(self):
        labels = self.epoched_labels  # .ravel()
        all_data = np.concatenate((labels, self.data_in_features), axis=1)
        train_data, test_data = train_test_split(all_data)

        if self.config.NEW_MODEL:
            self.classifier.fit(train_data)
        else:
            self.classifier.update(train_data)
        self.classifier.evaluate(test_data)

    # if given raw_data it will do the pipeline on it
    # if no data were given it will evoke the recorder
    def run_all(self, raw_data_path=''):
        if not raw_data_path:
            self.run_recording()
            self.raw_data = self.recorder.get_raw_data()
        else:
            self.raw_data = read_raw_fif(raw_data_path, preload=True)
        self.run_preprocessing()
        self.feature_selection()
        self.run_classifier()
