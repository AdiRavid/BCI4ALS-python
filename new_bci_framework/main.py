import os
from sys import path as sys_path
import random

from new_bci_framework.classifier.adaboost_classifier import AdaboostClassifier
from new_bci_framework.classifier.ensemble_classifier import EnsembleClassifier
from new_bci_framework.classifier.logistic_regression_classifier import LogisticRegressionClassifier
from new_bci_framework.classifier.random_forest_classifier import RandomforestClassifier
from new_bci_framework.classifier.xgb_classifier import XGBClassifier

full_path = os.path.abspath(__file__)
src_index = full_path.rfind('new_bci_framework')
path_to_root = full_path[: src_index]
if path_to_root not in sys_path:
    sys_path.append(path_to_root)
os.chdir(path_to_root)

from new_bci_framework.config.config import Config
from new_bci_framework.session.offline_session import OfflineSession
from new_bci_framework.recorder.open_bci_cyton_recorder import CytonRecorder, BoardIds
from new_bci_framework.ui.offline_ui import OfflineUI
from new_bci_framework.paradigm.MI_paradigm import MIParadigm
from new_bci_framework.preprocessing.preprocessing_pipeline import PreprocessingPipeline

import mne
from mne.io import read_raw_fif

search_path = os.path.join(os.getcwd(), "data", "Sivan")


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


def concat_files():
    raws = []
    for root, dir, files in os.walk(search_path):
        for file in files:
            if file.endswith(".fif") and 'Sivan' in file:
                file_full_path = os.path.join(root, file)
                raws.append(read_raw_fif(file_full_path, preload=True))

    concated_raw = mne.concatenate_raws(raws)

    concated_raw.save(os.path.join(search_path, "data", "Sivan", "sivan_all_files.csv"))


if __name__ == '__main__':
    synth = True  # TODO - Change for synthetic recording

    config = Config(num_trials=30, synth=synth)
    boardID = BoardIds.SYNTHETIC_BOARD if synth else BoardIds.CYTON_DAISY_BOARD
    session = OfflineSession(
        config=config,
        recorder=CytonRecorder(config, board_id=boardID),
        ui=OfflineUI(config),
        # ui=OfflineUI(config),
        paradigm=MIParadigm(config),
        preprocessor=PreprocessingPipeline(config),
        # classifier=DummyClassifier(config) # TODO: activate the classifier you want to use.
        # classifier=EnsembleClassifier(config)
        # classifier=RandomforestClassifier(config)
        # classifier = LogisticRegressionClassifier(config)
        classifier=XGBClassifier(config)
    )

    # TODO: activate to run on of: RandomforestClassifier, LogisticRegressionClassifier, XGBClassifier,
    #  and add path to directory that contains the fif files.
    session.run_all(raw_data_path=os.path.join("data\Sivan"))

    # TODO: activate to run on of: EnsembleClassifier, RandomForestEnsembleClassifier, LogisticRegressionEnsembleClassifier,
    #  and add path to directory that contains the fif files.
    # run_pipeline_for_directory(path=r"data\Sivan", session=session)
