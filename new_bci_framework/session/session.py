########################################################################################################################
#                                                      Imports                                                         #
########################################################################################################################
from new_bci_framework.config.config import Config
from new_bci_framework.recorder.recorder import Recorder
from new_bci_framework.ui.recording_ui.recording_ui import RecordingUI
from new_bci_framework.paradigm.paradigm import Paradigm
from new_bci_framework.preprocessing.preprocessing_pipeline import PreprocessingPipeline
from new_bci_framework.classifier.base_classifier import BaseClassifier


########################################################################################################################
#                                                   Implementation                                                     #
########################################################################################################################
class Session:
    """
    Base class for an EEG session, with online or offline recording, or analysis of previous recordings.
    Simple public api for creating and running the session.
    """
    def __init__(self, config: Config, recorder: Recorder, ui: RecordingUI,
                 paradigm: Paradigm, preprocessor: PreprocessingPipeline,
                 classifier: BaseClassifier):
        self.config = config
        self.recorder = recorder
        self.ui = ui
        self.paradigm = paradigm
        self.preprocessor = preprocessor
        self.classifier = classifier
        self.raw_data = None
        self.processed_data = None
        self.labels = None
        self.data_in_features = None

    def run_recording(self, save=True) -> None:
        """
        Runs the recording phase with the initiated paradigm.
        If save = True, then save the recorded data to the data directory.
        See :class:`Recorder`
        """
        self.recorder.start_recording()
        self.recorder.plot_live_data()
        self.run_paradigm()
        self.recorder.end_recording()

        if save:
            self.raw_data = self.recorder.get_raw_data()
            self.raw_data.save(f'new_bci_framework/../data/{self.config.SUBJECT_NAME}_{self.config.DATE}_raw.fif')

    def run_paradigm(self) -> None:
        """
        The main part of the recording phase, obtains the events from the Paradigm and runs the UI accordingly,
        while recording.
        See :class:`Paradigm` and :class: `RecordingUI`
        """
        raise NotImplementedError

    def run_preprocessing(self) -> None:
        """
        Runs the preprocessing pipeline which returns the preprocessed data - an ndarray of shape n_trials x n_features,
        and the labels - an ndarray of shape n_trials x 1.
        See :class:`PreprocessingPipeline`
        """
        self.processed_data, self.labels = self.preprocessor.run_pipeline(self.raw_data)

    def run_classifier(self) -> None:
        """
        Fits the classifier to the data.
        See :class:`BaseClassifier`
        """
        raise NotImplementedError

    def run_all(self, raw_data=None) -> None:
        """
        Runs the entire session - recording (if raw_data is None), preprocessing, classification.
        :param raw_data: An mne Raw object storing a recording session. If not None, session starts from after
        recording step.
        """
        if not raw_data:  # if no data given, evoke the recorder
            self.run_recording()
            self.raw_data = self.recorder.get_raw_data()
        else:  # if raw_data is given, skip recording
            self.raw_data = raw_data
        self.run_preprocessing()
        self.run_classifier()
