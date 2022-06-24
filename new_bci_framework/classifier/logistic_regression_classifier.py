import mne
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

import new_bci_framework.classifier.optuna_runner as op
from new_bci_framework.classifier.base_classifier import BaseClassifier
from new_bci_framework.config.config import Config
import xgboost as xgb
import numpy as np
import pickle
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier


class LogisticRegressionClassifier(BaseClassifier):
    """
    Logistic regression classifier.
    """

    def __init__(self, config: Config):
        super().__init__(config)
        self._model = None

    def fit(self, X: np.ndarray, y: np.ndarray):
        """
        fit model using the given data.
        we do feature selection over the data.
        we run optuna for finding best parameter for training.
        :param X: data
        :param y: labels
        :return: None
        """
        X = self.feature_selection(X, y)

        best_param = op.run_optuna_LR(X, y)
        self._model = LogisticRegression(solver='liblinear', **best_param)
        self._model.fit(X, y)

    def predict(self, X: np.ndarray):
        """
        make prediction over given data (use the same feature selection).
        :param X: data
        :return: predictions
        """
        X = self.selector.transform(X)
        return self._model.predict(X)

    def save_classifier(self):
        """
        save classifier to pickle.
        :return: None
        """
        pickle.dump(self._model, open(self._config.MODEL_PATH + "_LR", 'wb'))

    def load_classifier(self):
        """
        load classifier from pickle.
        :return: None
        """
        self._ensemble = pickle.load(open(self._config.MODEL_PATH + "_LR", 'rb'))
