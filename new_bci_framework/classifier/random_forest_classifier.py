import mne
from sklearn.ensemble import RandomForestClassifier

import new_bci_framework.classifier.optuna_runner as op
from new_bci_framework.classifier.base_classifier import BaseClassifier
from new_bci_framework.config.config import Config
import xgboost as xgb
import numpy as np
import pickle
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
class RandomforestClassifier(BaseClassifier):
    """
    Random Forest classifier
    """

    def __init__(self, config: Config):
        super().__init__(config)
        self._model = None

    ## fit model using the given data.
    ## we do feature selection over the data.
    ## we run optuna for finding best parameter for training.
    def fit(self, X: np.ndarray, y: np.ndarray):
        X = self.feature_selection(X, y)

        best_param = op.run_optuna_RF(X, y)
        self._model = RandomForestClassifier(**best_param)
        self._model.fit(X, y)

    ## make prediction over given data (use the same feature selection).
    def predict(self, X: np.ndarray):
        X = self.selector.transform(X)
        return self._model.predict(X)

    ## save classifier to pickle.
    def save_classifier(self):
        pickle.dump(self._model, open(self._config.MODEL_PATH + "_RF", 'wb'))
