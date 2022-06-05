from new_bci_framework.session.session import Session

from new_bci_framework.config.config import Config
from new_bci_framework.recorder.recorder import Recorder
from new_bci_framework.ui.ui import UI
from new_bci_framework.paradigm.paradigm import Paradigm
from new_bci_framework.preprocessing.preprocessing_pipeline import PreprocessingPipeline
from new_bci_framework.classifier.base_classifier import BaseClassifier


class FeedbackSession(Session):

    def __init__(self, config: Config, recorder: Recorder, ui: UI, paradigm: Paradigm,
                 preprocessor: PreprocessingPipeline, classifier: BaseClassifier):
        super().__init__(config, recorder, ui, paradigm, preprocessor, classifier)

    def run_paradigm(self):
        # events = self.paradigm.get_events()
        events = ['RIGHT', 'IDLE', 'LEFT', 'LEFT']
        work = len(events)

        self.ui.setup()

        for i in range(work):
            if self.ui.need_to_quit():
                break
            self.ui.clear_surface(self.ui.msg_surface)
            self.ui.display_event(self.recorder, events[i], self.ui.msg_surface)
            self.run_all()
            for t, p in zip(self.labels, self.classifier.predict(self.processed_data)):
                self.ui.display_prediction(t, p)

        self.ui.quit()

    def run_classifier(self):
        pass

    def run_all(self, data=None):
        data = self.recorder.get_partial_raw_data()
        super(FeedbackSession, self).run_all(data)


