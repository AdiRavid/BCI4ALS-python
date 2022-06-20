import mne
from new_bci_framework.config.config import Config
import xgboost as xgb
import numpy as np
import pickle
from sklearn.metrics import classification_report
import sklearn.linear_model as lm


class SGDClassifier:
    """
    Basic class for a classifier for session eeg data.
    API includes training, prediction and evaluation.
    """

    def __init__(self, config: Config):
        self._config = config
        self._model = lm.SGDClassifier()

    def fit(self, data: np.ndarray):
        self._model.fit(data[:, 1:], data[:, 0])
        pickle.dump(self._model, open(self._config.MODEL_PATH+"_SGD", 'wb'))

    def update(self, data: np.ndarray):
        self._model = pickle.load(open(self._config.MODEL_PATH+"_SGD", 'rb'))
        self._model.partial_fit(data[:, 1:], data[:, 0])

    def predict(self, data: np.ndarray):
        loaded_model = pickle.load(open(self._config.MODEL_PATH+"_SGD", 'rb'))
        prediction = loaded_model.predict(data)
        print("current predict: ", prediction)

    def evaluate(self, data: np.ndarray):
        loaded_model = pickle.load(open(self._config.MODEL_PATH+"_SGD", 'rb'))
        prediction = loaded_model.predict(data[:, 1:])
        print("----------------------------SGD:---------------------------")
        print(classification_report(data[:, 0], prediction))

    # pick features
    def feature_selection(self, config):
        pass
