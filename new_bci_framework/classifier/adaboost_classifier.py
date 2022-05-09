import mne
from new_bci_framework.config.config import Config
import xgboost as xgb
import numpy as np
import pickle
from sklearn.metrics import classification_report
from sklearn.ensemble import AdaBoostClassifier


class adaboost_classifier:
    """
    Basic class for a classifier for session eeg data.
    API includes training, prediction and evaluation.
    """

    def __init__(self, config: Config):
        self._config = config
        self._model = AdaBoostClassifier(n_estimators=100, random_state=0)

    def fit(self, data: np.ndarray):
        self._model.fit(data[:, 1:], data[:, 0])
        pickle.dump(self._model, open(self._config.MODEL_PATH + "_adaboost", 'wb'))

    def predict(self, data: np.ndarray):
        prediction = self._model.predict(data)
        print("current predict: ", prediction)

    def evaluate(self, data: np.ndarray):
        prediction = self._model.predict(data[:, 1:])
        print("-----------------------AdaBoost:--------------------------")
        print(classification_report(data[:, 0], prediction))
