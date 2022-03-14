from new_bci_framework.classifier.base_classifier import BaseClassifier
from new_bci_framework.recorder.test import main_test
from new_bci_framework.config.config import Config
from new_bci_framework.paradigm.p300_paradigm import P300Paradaigm
from new_bci_framework.preprocessing.preprocessing_pipeline import PreprocessingPipeline
from new_bci_framework.recorder.recorder import Recorder
from new_bci_framework.session.session import Session

if __name__ == '__main__':
    config = Config()

    config.SUBJECT_NAME = input("TEST_SUBJECT: ")

    session = Session(
        recorder=Recorder(config),
        paradigm=P300Paradaigm(config),
        preprocessor=PreprocessingPipeline(config),
        classifier=BaseClassifier(config),
        config=config
    )
    session.run_all()
    main_test()