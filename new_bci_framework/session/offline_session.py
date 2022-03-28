from new_bci_framework.session.session import Session
from new_bci_framework.recorder.recorder import Recorder
from new_bci_framework.classifier.base_classifier import BaseClassifier
from new_bci_framework.paradigm.paradigm import Paradigm
from new_bci_framework.preprocessing.preprocessing_pipeline import PreprocessingPipeline
from new_bci_framework.config.config import Config

from mne.io import read_raw_fif
from sklearn.model_selection import train_test_split


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

    def run_preprocessing(self, raw_data_path: str = ''):
        if not raw_data_path:
            self.raw_data = self.recorder.get_raw_data()
        else:
            self.raw_data = read_raw_fif(raw_data_path, preload=True)

        self.epoched_data = self.preprocessor.run_pipeline(self.raw_data)

    def feature_selection(self):
        pass

    def run_classifier(self):
        train_data, test_data = train_test_split(self.epoched_data)
        self.classifier.fit(train_data)
        evaluation = self.classifier.evaluate(test_data)

    def run_all(self):
        self.run_recording()
        self.run_preprocessing()
        self.feature_selection()
        # self.run_classifier()



