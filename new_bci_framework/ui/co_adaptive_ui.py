########################################################################################################################
#                                                      Imports                                                         #
########################################################################################################################
from new_bci_framework.ui.offline_ui import OfflineUI
from new_bci_framework.recorder.recorder import Recorder
from new_bci_framework.config.config import Config
from new_bci_framework.preprocessing.preprocessing_pipeline import PreprocessingPipeline
from new_bci_framework.classifier.base_classifier import BaseClassifier

import pygame as pg
from nptyping import NDArray


########################################################################################################################
#                                                   Implementation                                                     #
########################################################################################################################
class CoAdaptiveUI(OfflineUI):

    def __init__(self, config: Config, preprocessor: PreprocessingPipeline, model: BaseClassifier):
        super().__init__(config)
        self.preprocessor = preprocessor
        self.model = model

        self.num_trials_for_prediction = config.NUM_TRIALS_FOR_PREDICTION
        self.trial_counter = 0

    def run(self, recorder: Recorder, events: NDArray):
        super().run(recorder, events)

    def mainloop(self, recorder: Recorder):
        super().mainloop(recorder)

    def single_iter_work(self, recorder: Recorder):
        super().single_iter_work(recorder)
        # TODO - process data and update model when needed

    def _setup(self):
        pg.display.set_caption('Co-Adaptive Training Session')
        super()._setup()

    def _handle_event_end(self):
        # TODO - predict and display prediction
        # clear event:
        super()._handle_event_end()






