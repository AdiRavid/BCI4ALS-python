from mne.io import read_raw_fif
from new_bci_framework.classifier.sgd_classifier import SGDClassifier

from new_bci_framework.config.config import Config
from new_bci_framework.session.offline_session import OfflineSession
from new_bci_framework.recorder.open_bci_cyton_recorder import CytonRecorder, BoardIds
from new_bci_framework.paradigm.MI_paradigm import MIParadigm
from new_bci_framework.ui.offline_ui import OfflineUI
from new_bci_framework.preprocessing.preprocessing_pipeline import PreprocessingPipeline
from new_bci_framework.classifier.base_classifier import BaseClassifier
from new_bci_framework.classifier.adaboost_classifier import adaboost_classifier
import mne
import os

search_path = os.path.join(os.getcwd(), "..")


def concat_files():
    raws = []
    for root, dir, files in os.walk(search_path):
        for file in files:
            if file.endswith(".fif"):
                file_full_path = os.path.join(root, file)
                raws.append(read_raw_fif(file_full_path, preload=True))

    concated_raw = mne.concatenate_raws(raws)
    concated_raw.save(os.path.join(search_path, "data", "all_files.fif"))


if __name__ == '__main__':
    config = Config(name='Michael', num_trials=30)  # TODO- add selected_feature_path to use existing selected features.
    boardID = BoardIds.SYNTHETIC_BOARD  # TODO-change to BoardIds.CYTON_DAISY_BOARD when running real experiments
    # boardID = BoardIds.CYTON_DAISY_BOARD
    session = OfflineSession(
        config=config,
        recorder=CytonRecorder(config, board_id=boardID),  # TODO: change when running without recording
        # recorder=None,
        paradigm=MIParadigm(config, OfflineUI(config)),
        preprocessor=PreprocessingPipeline(config),
        classifier=BaseClassifier(config),
        sgd_classifier=SGDClassifier(config),
        adaboost_classifier=adaboost_classifier(config)

    )
    # session.run_recording()
    # concat_files()
    session.run_all(
        r"C:\Users\ASUS\Documents\BCI4ALS-python-new\data\all_data_up_to_may1_normed_no_CP6.fif")  # raw_data_path=os.path.join(search_path, "data", "all_files.fif"))
