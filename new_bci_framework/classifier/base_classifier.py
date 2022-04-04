import mne
from new_bci_framework.config.config import Config
import xgboost as xgb
import numpy as np
import pickle


class BaseClassifier:
    """
    Basic class for a classifier for session eeg data.
    API includes training, prediction and evaluation.
    """

    def __init__(self, config: Config):
        self._config = config
        self._model = xgb.XGBClassifier(n_estimators=177, max_depth=7, learning_rate=0.786, colsample_bytree=0.114,
                                        alpha=4.836, booster='dart', tree_method='approx', importance_type='gain')

    def fit(self, data: np.ndarray):
        self._model.fit(data[:, 1:], data[:, 0])
        pickle.dump(self._model, open(self._config.MODEL_PATH, 'wb'))

    def update(self, data: np.ndarray):
        loaded_model = pickle.load(open(self._config.MODEL_PATH, 'rb'))
        self._model.fit(data[:, 1:], data[:, 0], xgb_model=loaded_model)

    def predict(self, data: np.ndarray):
        loaded_model = pickle.load(open(self._config.MODEL_PATH, 'rb'))
        prediction = loaded_model.predict(data)
        print("current predict: ", prediction)

    def evaluate(self, data: np.ndarray):
        loaded_model = pickle.load(open(self._config.MODEL_PATH, 'rb'))
        prediction = loaded_model.predict(data[:, 1:])

    # pick features
    def feature_selection(self, config):
        pass
