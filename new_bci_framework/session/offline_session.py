from new_bci_framework.session.session import Session
from new_bci_framework.recorder.recorder import Recorder
from new_bci_framework.classifier.base_classifier import BaseClassifier
from new_bci_framework.paradigm.paradigm import Paradigm
from new_bci_framework.preprocessing.preprocessing_pipeline import PreprocessingPipeline
from new_bci_framework.config.config import Config
import numpy as np

from mne.io import read_raw_fif
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, f_classif


class OfflineSession(Session):
    """
    Subclass of session for an offline recording session.
    """

    def __init__(self, config: Config, recorder: Recorder, paradigm: Paradigm,
                 preprocessor: PreprocessingPipeline,
                 classifier: BaseClassifier):
        super().__init__(config, recorder, paradigm,
                         preprocessor, classifier)

    def run_recording(self, save=True):
        self.recorder.start_recording()
        self.paradigm.start(self.recorder)
        self.recorder.end_recording()

        if save:
            self.raw_data = self.recorder.get_raw_data()
            self.raw_data.save(f'../data/{self.config.SUBJECT_NAME}_{self.config.DATE}_raw.fif')

    def run_preprocessing(self):
        self.epoched_data,  self.epoched_labels = self.preprocessor.run_pipeline(self.raw_data)
        #self.preprocessor.run_pipeline(self.raw_data)


    # chose features
    # data is of size (n_epochs, n_features)
    # labels is of size n_epochs
    def feature_selection(self):
        num_of_features = self.config.NUM_OF_FEATURES

        X = self.epoched_data
        y = self.epoched_labels.ravel()
        self.data_in_features = SelectKBest(score_func=f_classif, k=num_of_features).fit_transform(X, y)

    def run_classifier(self):
        labels =  self.epoched_labels.ravel()
        all_data = np.concatenate((labels, self.data_in_features), axis=1)
        train_data, test_data = train_test_split(all_data)
        self.classifier.fit(train_data)
        evaluation = self.classifier.evaluate(test_data)

    # if given raw_data it will do the pipeline on it
    # if no data were given it will evoke the recorder
    def run_all(self, raw_data_path=''):
        if not raw_data_path:
            self.run_recording()
            self.raw_data = self.recorder.get_raw_data()
        else:
            self.raw_data = read_raw_fif(raw_data_path, preload=True)
        self.run_preprocessing()
        data_in_features = self.feature_selection()
        self.run_classifier()



