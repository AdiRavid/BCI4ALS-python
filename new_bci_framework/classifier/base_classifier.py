import mne
from new_bci_framework.config.config import Config


class BaseClassifier:
    """
    Basic class for a classifier for session eeg data.
    API includes training, prediction and evaluation.
    """

    def __init__(self, config: Config):
        pass

    def fit(self, data: mne.Epochs):
        pass

    def update(self, data: mne.Epochs):
        pass

    def predict(self, data: mne.Epochs):
        pass

    def evaluate(self, data: mne.Epochs):
        pass

    # pick features
    def feature_selection(self,config):
        pass
