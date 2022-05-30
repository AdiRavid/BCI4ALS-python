from new_bci_framework.classifier.sgd_classifier import SGDClassifier
from new_bci_framework.config.config import Config
from new_bci_framework.recorder.recorder import Recorder
from new_bci_framework.ui.ui import UI
from new_bci_framework.paradigm.paradigm import Paradigm
from new_bci_framework.classifier.base_classifier import BaseClassifier
from new_bci_framework.classifier.adaboost_classifier import adaboost_classifier

from new_bci_framework.preprocessing.preprocessing_pipeline import PreprocessingPipeline


class Session:
    """
    Base class for an EEG session, with online or offline recording, or analysis of previous recordings.
    simple public api for creating and running the session.
    """

    def __init__(self, config: Config, recorder: Recorder, ui: UI,
                 paradigm: Paradigm, preprocessor: PreprocessingPipeline,
                 classifier: BaseClassifier):
        self.config = config
        self.recorder = recorder
        self.ui = ui
        self.paradigm = paradigm
        self.preprocessor = preprocessor
        self.classifier = classifier
        self.raw_data = None
        self.epoched_data = None
        self.epoched_labels = None
        self.data_in_features = None

    def run_all(self, raw_data_path=''):
        pass

    @staticmethod
    def load_session(session_dir: str):
        """
        Load a previously recorded session from disk to preform analysis.
        :param session_dir: saved session directory
        :return: Session object
        """
