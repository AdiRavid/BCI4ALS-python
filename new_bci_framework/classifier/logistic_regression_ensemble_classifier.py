import numpy as np
import xgboost as xgb
from sklearn.metrics import classification_report

import new_bci_framework.classifier.optuna_runner as op
from new_bci_framework.classifier.base_classifier import BaseClassifier
from new_bci_framework.config.config import Config
import pickle

from sklearn.linear_model import LogisticRegression


class LogisticRegressionEnsembleClassifier(BaseClassifier):

    def __init__(self, config: Config):
        super().__init__(config)
        self._ensemble = None

    def fit(self, X: np.ndarray, y: np.ndarray):
        self._ensemble = self._ensemble if self._ensemble else []
        X = self.feature_selection(X, y)

        best_param = op.run_optuna_LR(X, y)
        new_classifier = LogisticRegression(solver='liblinear', **best_param)
        new_classifier.fit(X, y)
        self._ensemble.append(new_classifier)

    def _count_classes(self, prediction):
        return np.argmax([(prediction == i).sum() for i in [1, 2, 3]]) + 1

    def predict(self, X: np.ndarray):
        X = self.selector.transform(X)

        ensemble_prediction = np.ndarray((len(self._ensemble), X.shape[0]))
        for i, current_classifier in enumerate(self._ensemble):
            ensemble_prediction[i] = current_classifier.predict(X)
        # ensemble_prediction = ensemble_prediction
        prediction = np.apply_along_axis(func1d=self._count_classes, axis=0, arr=ensemble_prediction)

        return prediction.reshape((prediction.shape[0], 1))

    # not relevant to this classifier
    def update(self, X: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    def save_classifier(self):
        pickle.dump(self._ensemble, open(self._config.MODEL_PATH + "_EnsembleLR", 'wb'))

    def load_classifier(self):
        self._ensemble = pickle.load(open(self._config.MODEL_PATH + "_EnsembleLR", 'rb'))

    def evaluate(self, X: np.ndarray, y: np.ndarray):
        # transform is called in predict
        # X = self.selector.transform(X)
        self.save_classifier()
        prediction = self.predict(X)
        print("----------------------- EVALUATION --------------------------")
        x = classification_report(y, prediction)
        print(x)
        pickle.dump(self._ensemble, open(f"xgb_ensemble_LR", 'wb'))
