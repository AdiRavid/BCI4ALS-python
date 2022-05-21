import mne
from new_bci_framework.config.config import Config
import xgboost as xgb
import numpy as np
import pickle
from sklearn.metrics import classification_report


class XGBClassifier:
    """
    Basic class for a classifier for session eeg data.
    API includes training, prediction and evaluation.
    """

    def __init__(self, config: Config):
        self._config = config
        # self._model = xgb.XGBClassifier(n_estimators=144, max_depth=47, learning_rate=0.199, colsample_bytree= 0.309,
        # alpha=5.6204, booster='gbtree', tree_method='exact', importance_type='weight')
        self._model = xgb.XGBClassifier(n_estimators=185, max_depth=9, learning_rate=0.8052, colsample_bytree= 0.4073,
                alpha=3.0899, booster='dart', tree_method='exact', importance_type='total_gain')



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
        print("-----------------------XGB:--------------------------")
        print(classification_report(data[:, 0], prediction))


    # pick features
    def feature_selection(self, config):
        pass
