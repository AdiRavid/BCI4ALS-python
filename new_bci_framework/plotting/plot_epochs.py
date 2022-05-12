from mne.io import read_raw_fif
from new_bci_framework.config.config import Config
from new_bci_framework.session.offline_session import OfflineSession
from new_bci_framework.recorder.open_bci_cyton_recorder import CytonRecorder, BoardIds
from new_bci_framework.paradigm.paradigm import Paradigm
from new_bci_framework.preprocessing.preprocessing_pipeline import PreprocessingPipeline

def plot_epochs(raw_data_path, run_filter=False):
    config = Config(name='Michael', num_trials=30)  # TODO- add selected_feature_path to use existing selected features.
    boardID = BoardIds.SYNTHETIC_BOARD  # TODO-change to BoardIds.CYTON_DAISY_BOARD when running real experiments
    # boardID = BoardIds.CYTON_DAISY_BOARD
    session = OfflineSession(
        config=config,
        recorder=CytonRecorder(config, board_id=boardID),  # TODO: change when running without recording
        # recorder=None,
        paradigm=Paradigm(config),
        preprocessor=PreprocessingPipeline(config),
    )
    raw = read_raw_fif(raw_data_path, preload=True)
    raw.plot_psd()
    if run_filter:
        session.preprocessor._filter(raw)
    epochs = session.preprocessor._segment(raw)
    epochs['LEFT'].plot_psd(picks='eeg')
    epochs['RIGHT'].plot_psd(picks='eeg')
    epochs['IDLE'].plot_psd(picks='eeg')

    epochs['LEFT'].plot_image(picks='eeg', combine='mean')
    epochs['RIGHT'].plot_image(picks='eeg', combine='mean')
    epochs['IDLE'].plot_image(picks='eeg', combine='mean')



plot_epochs("../../data/Michael_2022-04-28-18-33_raw.fif")
