from mne.io import read_raw_fif
from new_bci_framework.classifier.sgd_classifier import SGDClassifier

from new_bci_framework.config.config import Config
from new_bci_framework.session.offline_session import OfflineSession
from new_bci_framework.recorder.opeb_bci_cyton_recorder import CytonRecorder, BoardIds
from new_bci_framework.paradigm.MI_paradigm import MIParadigm
from new_bci_framework.ui.offline_ui import OfflineUI
from new_bci_framework.preprocessing.preprocessing_pipeline import PreprocessingPipeline
from new_bci_framework.classifier.base_classifier import BaseClassifier
import mne

#TODO: make generic (look for files then concat them)
def concat_files():
    d1 = r"C:\Users\ASUS\Documents\BCI4ALS-python-new\data\Synth_2022-04-04-10-02_raw_5_trials.fif"
    d2 = r"C:\Users\ASUS\Documents\BCI4ALS-python-new\data\Synth_2022-04-04-10-09_raw_20_trials.fif"
    d3 = r"C:\Users\ASUS\Documents\BCI4ALS-python-new\data\Synth_2022-04-04-10-51_raw_35_trials.fif"
    d4 = r"C:\Users\ASUS\Documents\BCI4ALS-python-new\data\Synth_2022-04-04-11-06_raw_20_trials.fif"

    r1 = read_raw_fif(d1, preload=True)
    r2 = read_raw_fif(d2, preload=True)
    r3 = read_raw_fif(d3, preload=True)
    r4 = read_raw_fif(d4, preload=True)

    concated_raw = mne.concatenate_raws([r1, r2, r3, r4])
    concated_raw.save(r"C:\Users\ASUS\Documents\BCI4ALS-python-new\data\all_files.fif")


if __name__ == '__main__':
    config = Config(num_trials=20)
    # boardID = BoardIds.SYNTHETIC_BOARD  # TODO-change to BoardIds.CYTON_BOARD when running real experiments
    boardID = BoardIds.CYTON_BOARD
    session = OfflineSession(
        # recorder=CytonRecorder(config, board_id=boardID),  # TODO: change when running without recording
        recorder=None,
        paradigm=MIParadigm(config, OfflineUI(config)),
        preprocessor=PreprocessingPipeline(config),
        classifier=BaseClassifier(config),
        config=config,
        sgd_classifier=SGDClassifier(config)
    )
    session.run_all(raw_data_path=r"C:\Users\ASUS\Documents\BCI4ALS-python-new\data\all_files.fif")


    # concat_files()