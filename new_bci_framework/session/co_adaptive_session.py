from new_bci_framework.session.session import Session
from new_bci_framework.recorder.recorder import Recorder
from new_bci_framework.classifier.base_classifier import BaseClassifier
from new_bci_framework.paradigm.paradigm import Paradigm
from new_bci_framework.preprocessing.preprocessing_pipeline import PreprocessingPipeline
from new_bci_framework.config.config import Config

from sklearn.model_selection import train_test_split


class CoAdaptiveSession(Session):

    def __init__(self, config: Config, recorder: Recorder, paradigm: Paradigm, preprocessor: PreprocessingPipeline,
                 classifier: BaseClassifier):
        super().__init__(config, recorder, paradigm, preprocessor, classifier)

    def run_all(self):
        super().run_all()
