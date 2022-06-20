from mne.io import read_raw_fif
from new_bci_framework.config.config import Config
from new_bci_framework.session.offline_session import OfflineSession
from new_bci_framework.recorder.open_bci_cyton_recorder import CytonRecorder, BoardIds
from new_bci_framework.preprocessing.preprocessing_pipeline import PreprocessingPipeline
from new_bci_framework.paradigm.MI_paradigm import MIParadigm
from new_bci_framework.classifier.ensemble_classifier import EnsembleClassifier


# change these parameters:
raw_data_path = "/Users/maysanb/PycharmProjects/BCI4ALS-python/data/Sivan_2022-05-29-12-16_raw.fif"
run_filter = True # if true, preprocessing (filtering) will run before plotting


def plot_epochs(raw_data_path, run_filter=False):
    config = Config(num_trials=30, synth= True)
    boardID = BoardIds.SYNTHETIC_BOARD
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

    epochs['LEFT'].plot_image(combine='mean')
    epochs['RIGHT'].plot_image(combine='mean')
    epochs['IDLE'].plot_image(combine='mean')


plot_epochs(raw_data_path, run_filter)
