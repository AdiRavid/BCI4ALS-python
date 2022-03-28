from new_bci_framework.config.config import Config
from new_bci_framework.session.offline_session import OfflineSession
from new_bci_framework.recorder.opeb_bci_cyton_recorder import CytonRecorder, BoardIds
from new_bci_framework.paradigm.MI_paradigm import MIParadigm
from new_bci_framework.ui.offline_ui import OfflineUI
from new_bci_framework.preprocessing.preprocessing_pipeline import PreprocessingPipeline
from new_bci_framework.classifier.base_classifier import BaseClassifier


from mne.io import read_raw_fif

if __name__ == '__main__':
    config = Config()
    raw_data = read_raw_fif('/Users/maysanb/PycharmProjects/BCI4ALS-python/data/Synth_2022-03-16_raw.fif', preload=True);
    session = OfflineSession(
        recorder=CytonRecorder(config, board_id=BoardIds.SYNTHETIC_BOARD),
        paradigm=MIParadigm(config, OfflineUI(config)),
        preprocessor=PreprocessingPipeline(config),
        classifier=BaseClassifier(config),
        config=config
    )
    #session.run_recording()
    session.run_preprocessing(raw_data)
