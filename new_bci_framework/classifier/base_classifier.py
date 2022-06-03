import numpy as np
import pickle
from os import path

from new_bci_framework.config.config import Config
from sklearn.feature_selection import SelectKBest, mutual_info_classif


class BaseClassifier:
    """
    Basic class for a classifier for session eeg data.
    API includes training, prediction and evaluation.
    """

    def __init__(self, config: Config):
        self._config = config
        self.selector = None

    def feature_selection(self, X, y):
        num_of_features = self._config.NUM_OF_FEATURES
        self.selector = SelectKBest(score_func=mutual_info_classif, k=num_of_features)
        return self.selector.fit_transform(X, y)

    def save_features(self):
        indices = self.selector.get_support(indices=True)
        pickle.dump(indices, open("feature_selection", 'wb'))
        # also save as txt for debug
        np.savetxt(path.join("preprocessing", self._config.DATE + "_selected_features.txt"),
                   indices, delimiter='\n', fmt='%s')

    def fit(self, X: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    def predict(self, X: np.ndarray):
        raise NotImplementedError

    def update(self, X: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    def evaluate(self, X: np.ndarray, y: np.ndarray):
        raise NotImplementedError
