from new_bci_framework.session.session import Session

from new_bci_framework.config.config import Config
from new_bci_framework.recorder.recorder import Recorder
from new_bci_framework.ui.recording_ui.recording_ui import RecordingUI
from new_bci_framework.paradigm.paradigm import Paradigm
from new_bci_framework.preprocessing.preprocessing_pipeline import PreprocessingPipeline
from new_bci_framework.classifier.base_classifier import BaseClassifier


class FeedbackSession(Session):
    """
    Subclass of session for a feedback recording session.
    In this session the classifier is pre-trained (loaded from pickle) and for each recorded trial the prediction is
    displayed.
    """
    def __init__(self, config: Config, recorder: Recorder, ui: RecordingUI, paradigm: Paradigm,
                 preprocessor: PreprocessingPipeline, classifier: BaseClassifier):
        super().__init__(config, recorder, ui, paradigm, preprocessor, classifier)
        self.classifier.load_classifier()
        self.data = None

    def run_paradigm(self):
        """
        see :func:'run_paradigm <new_bci_framework.session.Session.run_paradigm>'
        In addition, this method also runs preprocessing and classifier predictions on each event, to present to the
        subject and creat a neuro-feedback loop.
        """
        events = self.paradigm.get_events()
        work = len(events)

        self.ui.setup()

        for i in range(work):
            if self.ui.need_to_quit():
                break
            self.ui.clear_surface(self.ui.msg_surface)
            self.ui.display_event(self.recorder, events[i], self.ui.msg_surface)
            self.run_preprocessing()
            for t, p in zip(self.labels, self.classifier.predict(self.processed_data)):
                self.ui.display_prediction(t, p)

        self.ui.quit()

    def run_preprocessing(self) -> None:
        """
        see :func:'run_preprocessing <new_bci_framework.session.Session.run_preprocessing>'
        Uses the super class's implementation on data from a single trial.
        """
        self.raw_data = self.recorder.get_partial_raw_data()
        super(FeedbackSession, self).run_preprocessing()

    def run_classifier(self) -> None:
        """
        Currently we are skipping this step and retraining separately from recording, but this method can implement
        updating the trained classifier with the new data recorded in this session.
        """
        pass
