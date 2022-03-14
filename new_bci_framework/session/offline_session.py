from session import Session
from new_bci_framework.recorder.recorder import Recorder
from new_bci_framework.recorder.opeb_bci_cyton_recorder import *
from new_bci_framework.classifier.base_classifier import BaseClassifier
from new_bci_framework.paradigm.paradigm import Paradigm
from new_bci_framework.paradigm.MI_paradigm import MIParadigm
from new_bci_framework.preprocessing.preprocessing_pipeline import PreprocessingPipeline
from new_bci_framework.config.config import Config


class OfflineSession(Session):
    """
    Subclass of session for an offline recording session.
    """

    def __init__(self, recorder: Recorder, paradigm: Paradigm,
                 # preprocessor: PreprocessingPipeline,
                 # classifier: BaseClassifier,
                 config: Config):
        super().__init__(recorder, paradigm,
                         # preprocessor, classifier,
                         config)

    def run_recording(self):
        self.recorder.start_recording()
        self.paradigm.start(self.recorder)
        data = self.recorder.get_raw_data()
        print()
        self.recorder.end_recording()

    # def run_preprocessing(self):
    #     self.raw_data = self.recorder.get_raw_data()
    #     self.epoched_data = self.preprocessor.run_pipeline(self.raw_data)
    #
    # def run_classifier(self):
    #     train_data, test_data = train_test_split(self.epoched_data)
    #     self.classifier.fit(train_data)
    #     evaluation = self.classifier.evaluate(test_data)
    #
    # def run_all(self):
    #     self.run_recording()
    #     self.run_preprocessing()
    #     self.run_classifier()


if __name__ == '__main__':
    config = Config()
    session = OfflineSession(CytonRecorder(None, BoardIds.SYNTHETIC_BOARD),
                             MIParadigm(config), config)
    session.run_recording()
    print()

