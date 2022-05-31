import os
import sys
import random

from new_bci_framework.classifier.ensemble_2_classes_classifier import Ensemble2ClassesClassifier
from new_bci_framework.classifier.ensemble_classifier import EnsembleClassifier
from new_bci_framework.classifier.knn_ensemble_classifier import KnnEnsembleClassifier
from new_bci_framework.classifier.sgd_classifier import SgdClassifier
from new_bci_framework.classifier.xgb_classifier import XGBClassifier

full_path = os.path.abspath(__file__)
src_index = full_path.rfind('new_bci_framework')
path_to_root = full_path[: src_index]
if path_to_root not in sys.path:
    sys.path.append(path_to_root)
os.chdir(path_to_root)

from new_bci_framework.config.config import Config
from new_bci_framework.session.offline_session import OfflineSession
from new_bci_framework.recorder.open_bci_cyton_recorder import CytonRecorder, BoardIds
from new_bci_framework.ui.offline_ui import OfflineUI
from new_bci_framework.paradigm.MI_paradigm import MIParadigm
from new_bci_framework.preprocessing.preprocessing_pipeline import PreprocessingPipeline
from new_bci_framework.classifier.base_classifier import BaseClassifier

import mne
from mne.io import read_raw_fif

search_path = os.path.join(os.getcwd(), "..", "data", "Sivan")


def run_pipeline_for_directory(path, session):
    files = (list(filter(lambda f: f.endswith(".fif"), os.listdir(os.path.join(os.getcwd(), path)))))
    random.shuffle(files)
    for idx, file in enumerate(files):
        print(f"<--- Start process file {idx}: {file} --->")
        if idx == (len(files) - 1):
            session.run_all_without_classifier(
                raw_data_path=os.path.join(os.getcwd(), path, file))
        else:
            session.run_all(raw_data_path=os.path.join(os.getcwd(), path, file))


def concat_files():
    raws = []
    for root, dir, files in os.walk(search_path):
        for file in files:
            if file.endswith(".fif") and 'Michael' in file:
                file_full_path = os.path.join(root, file)
                raws.append(read_raw_fif(file_full_path, preload=True))

    concated_raw = mne.concatenate_raws(raws)
    concated_raw.save(os.path.join(search_path, "data", "Sivan", "all_files.fif"))


if __name__ == '__main__':
    synth = True  # TODO - Change for synthetic recording

    config = Config(num_trials=30, synth=synth)  # TODO- add selected_feature_path to use existing selected features.
    boardID = BoardIds.SYNTHETIC_BOARD if synth else BoardIds.CYTON_DAISY_BOARD
    session = OfflineSession(
        config=config,
        recorder=CytonRecorder(config, board_id=boardID),
        ui=OfflineUI(config),
        paradigm=MIParadigm(config),
        preprocessor=PreprocessingPipeline(config),
        classifier=EnsembleClassifier(config)
    )
    # session.run_recording()
    # concat_files()
    # session.run_all(raw_data_path=os.path.join(search_path, "data", "all_files.fif"))
    run_pipeline_for_directory(path=r"data\Sivan", session=session)
