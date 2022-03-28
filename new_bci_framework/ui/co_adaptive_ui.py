########################################################################################################################
#                                                      Imports                                                         #
########################################################################################################################
from new_bci_framework.ui.offline_ui import UI
from new_bci_framework.recorder.recorder import Recorder
from new_bci_framework.config.config import Config
from new_bci_framework.preprocessing.preprocessing_pipeline import PreprocessingPipeline
from new_bci_framework.classifier.base_classifier import BaseClassifier

import pygame as pg
from nptyping import NDArray


########################################################################################################################
#                                                   Implementation                                                     #
########################################################################################################################
class CoAdaptiveUI(UI):

    def __init__(self, config: Config):
        super().__init__(config)

    def setup(self):
        super().setup()

    def display_event(self, label: str) -> None:
        super().display_event(label)