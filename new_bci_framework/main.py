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


# search_path = os.path.join(os.getcwd(), "data", "Sivan")


def run_pipeline_for_directory(path, session):
    files = (list(filter(lambda f: f.endswith(".fif"), os.listdir(os.path.join(os.getcwd(), path)))))
    random.shuffle(files)
    for idx, file in enumerate(files):
        print(f"<--- Start process file {idx}: {file} --->")
        if idx == (len(files) - 1):
            session.run_all_without_classifier(
                raw_data_path=os.path.join(os.getcwd(), path, file))
        else:
            session.run_all_for_ensammble(raw_data_path=os.path.join(os.getcwd(), path, file))


def concat_files(search_path):
    raws = []
    for root, dir, files in os.walk(search_path):
        for file in files:
            if file.endswith(".fif") and 'Sivan' in file:
                file_full_path = os.path.join(root, file)
                raws.append(read_raw_fif(file_full_path, preload=True))

    concated_raw = mne.concatenate_raws(raws)

    concated_raw.save(os.path.join(search_path, "data", "Sivan", "sivan_all_files.csv"))


if __name__ == '__main__':
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

