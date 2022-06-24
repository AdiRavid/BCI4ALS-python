import new_bci_framework.classifier.optuna_runner as op
from new_bci_framework.classifier.base_classifier import BaseClassifier
from new_bci_framework.config.config import Config
import xgboost as xgb
import numpy as np
import pickle


class XGBClassifier(BaseClassifier):
    """
    XGB classifier.
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

        best_param = op.run_optuna_xgb(X, y)
        self._model = xgb.XGBClassifier(best_param)
        self._model.fit(X, y)

    def predict(self, X: np.ndarray):
        """
        make prediction over given data (use the same feature selection).
        :param X: data
        :return: prediction
        """
        X = self.selector.transform(X)
        return self._model.predict(X)


    def save_classifier(self):
        """
        save classifier to pickle.
        :return: None
        """
        pickle.dump(self._model, open(self._config.MODEL_PATH + "_XGB", 'wb'))

    def load_classifier(self):
        """
        load classifier from pickle.
        :return: None
        """
        self._ensemble = pickle.load(open(self._config.MODEL_PATH + "_XGB", 'rb'))
