from new_bci_framework.config.config import Config
from new_bci_framework.recorder.recorder import Recorder
from new_bci_framework.recording_ui.recording_ui import RecordingUI
from new_bci_framework.paradigm.paradigm import Paradigm
from new_bci_framework.preprocessing.preprocessing_pipeline import PreprocessingPipeline
from new_bci_framework.classifier.base_classifier import BaseClassifier


class Session:
    """
    Base class for an EEG session, with online or offline recording, or analysis of previous recordings.
    simple public api for creating and running the session.
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
        self.filename = ""
        self.save = True

    def run_recording(self):
        self.recorder.start_recording()
        self.recorder.plot_live_data()
        self.run_paradigm()
        self.recorder.end_recording()

        if self.save:
            self.raw_data = self.recorder.get_raw_data()
            self.raw_data.save(f'new_bci_framework/../data/{self.config.SUBJECT_NAME}_{self.config.DATE}_raw.fif')

    def run_paradigm(self):
        raise NotImplementedError

    def run_preprocessing(self):
        self.processed_data, self.labels = self.preprocessor.run_pipeline(self.raw_data)

    def run_classifier(self):
        raise NotImplementedError

    def run_all(self, raw_data=None):
        if not raw_data:  # if no data given, evoke the recorder
            self.run_recording()
            self.raw_data = self.recorder.get_raw_data()
        else:  # if raw_data is given, skip recording
            self.raw_data = raw_data

        # self.filename = self.raw_data.filenames[0].split('/')[-1].split('.')[0]
        self.run_preprocessing()
        self.run_classifier()

    @staticmethod
    def load_session(session_dir: str):
        """
        Load a previously recorded session from disk to preform analysis.
        :param session_dir: saved session directory
        :return: Session object
        """
