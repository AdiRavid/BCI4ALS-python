from mne.io import read_raw_fif
from new_bci_framework.config.config import Config
from new_bci_framework.session.offline_session import OfflineSession
from new_bci_framework.recorder.open_bci_cyton_recorder import CytonRecorder, BoardIds
from new_bci_framework.paradigm.paradigm import Paradigm
from new_bci_framework.preprocessing.preprocessing_pipeline import PreprocessingPipeline
from new_bci_framework.ui.offline_ui import OfflineUI
from new_bci_framework.paradigm.MI_paradigm import MIParadigm
from new_bci_framework.classifier.ensemble_classifier import EnsembleClassifier

def plot_epochs(raw_data_path, run_filter=False):
    config = Config(num_trials=30, synth= True)
    boardID = BoardIds.SYNTHETIC_BOARD  # TODO-change to BoardIds.CYTON_DAISY_BOARD when running real experiments
    # boardID = BoardIds.CYTON_DAISY_BOARD
    session = OfflineSession(
        config=config,
        recorder=CytonRecorder(config, board_id=boardID),
        ui=None,
        paradigm=MIParadigm(config),
        preprocessor=PreprocessingPipeline(config),
        classifier=EnsembleClassifier(config)
    )
    raw = read_raw_fif(raw_data_path, preload=True)
    raw.plot_psd()
    if run_filter:
        raw = session.preprocessor._filter(raw)
    epochs = session.preprocessor._segment(raw)
    epochs['LEFT'].plot_psd(picks='eeg')
    epochs['RIGHT'].plot_psd(picks='eeg')
    epochs['IDLE'].plot_psd(picks='eeg')

    epochs['LEFT'].plot_image(picks='eeg', combine='mean')
    epochs['RIGHT'].plot_image(picks='eeg', combine='mean')
    epochs['IDLE'].plot_image(picks='eeg', combine='mean')

    #session.preprocessor._reject()

plot_epochs("/Users/maysanb/PycharmProjects/BCI4ALS-python/data/Sivan_2022-05-29-12-07_raw.fif")
