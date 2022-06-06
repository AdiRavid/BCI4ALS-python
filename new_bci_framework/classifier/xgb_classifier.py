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


class XGBClassifier(BaseClassifier):
    """
    Basic class for a classifier for session eeg data.
    API includes training, prediction and evaluation.
    """

    def __init__(self, config: Config):
        super().__init__(config)
        self._model = None

    def fit(self, X: np.ndarray, y: np.ndarray):
        X = self.feature_selection(X, y)

        best_param = op.run_optuna_xgb(X, y)
        # best_param ={'n_estimators': 168, 'max_depth': 41, 'learning_rate': 0.8377888847702736, 'colsample_bytree': 0.03332290674009903, 'alpha': 0.7944467940987507, 'booster': 'gbtree', 'tree_method': 'hist', 'importance_type': 'total_cover'}
        self._model = xgb.XGBClassifier(best_param)
        # self._model = RandomForestClassifier(n_estimators=5, max_depth=3)
        # self._model = SVC()
        self._model.fit(X, y)

    def predict(self, X: np.ndarray):
        X = self.selector.transform(X)
        return self._model.predict(X)

    def save_classifier(self):
        pickle.dump(self._model, open(self._config.MODEL_PATH + "_XGB", 'wb'))
