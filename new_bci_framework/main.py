import os
import sys

# Add root to path:
full_path = os.path.abspath(__file__)
src_index = full_path.rfind('new_bci_framework')
path_to_root = full_path[: src_index]
if path_to_root not in sys.path:
    sys.path.append(path_to_root)
os.chdir(path_to_root)

import random
import mne
from mne.io import read_raw_fif

# General
from new_bci_framework.config.config import Config
from new_bci_framework.recorder.cyton_recorder import CytonRecorder, BoardIds
from new_bci_framework.paradigm.MI_paradigm import MIParadigm
from new_bci_framework.preprocessing.preprocessing_pipeline import PreprocessingPipeline
from new_bci_framework.classifier.xgb_classifier import XGBClassifier
from new_bci_framework.classifier.dummy_classifier import DummyClassifier

# Offline session
from new_bci_framework.session.offline_session import OfflineSession
from new_bci_framework.ui.recording_ui.offline_recording_ui import OfflineRecordingUI

# Feedback session
from new_bci_framework.session.feedback_session import FeedbackSession
from new_bci_framework.ui.recording_ui.feedback_recording_ui import FeedbackRecordingUI


if __name__ == '__main__':
    # Currently the main is running offline recording.
    synth = False  # TODO - Change for synthetic recording

    config = Config(num_trials=30, synth=synth)
    boardID = BoardIds.SYNTHETIC_BOARD if synth else BoardIds.CYTON_DAISY_BOARD
    session = FeedbackSession(
        config=config,
        recorder=CytonRecorder(config, board_id=boardID),
        ui=FeedbackRecordingUI(config),
        paradigm=MIParadigm(config),
        preprocessor=PreprocessingPipeline(config),
        classifier=DummyClassifier(config)
    )

    session.run_recording()

