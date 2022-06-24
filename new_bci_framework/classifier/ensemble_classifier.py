import numpy as np
import xgboost as xgb
from sklearn.metrics import classification_report

import new_bci_framework.classifier.optuna_runner as op
from new_bci_framework.classifier.base_classifier import BaseClassifier
from new_bci_framework.config.config import Config
import pickle


class EnsembleClassifier(BaseClassifier):
    """
    Ensemble classifier of xgb models.
    the ensamble is an array of xgb model, that decide using the "major vote".
    """

    def __init__(self, config: Config):
        super().__init__(config)
        self._ensemble = None

    def fit(self, X: np.ndarray, y: np.ndarray):
        """
        fit a new xgb model and add it to the ensamble. we do feature selection, and save the paramters for later train
        and prediction. the model is trained with after running optuna that finds the best parameters.
        :param X: data
        :param y: labels
        :return: None
        """
        self._ensemble = self._ensemble if self._ensemble else []
        if self._ensemble: # think about saving features for each model individually and using them in the prediction
            # instead of using the same set of features for each recording
            X = self.selector.transform(X)
        else: X = self.feature_selection(X, y)
        best_param = op.run_optuna_xgb(X, y)
        new_classifier = xgb.XGBClassifier(best_param)
        new_classifier.fit(X, y)
        self._ensemble.append(new_classifier)

    def _count_classes(self, prediction):
        """
        find the majority vote for each prediction.
        :param prediction: prediction by ensemble
        :return: majority vote for the prediction
        """
        return np.argmax([(prediction == i).sum() for i in [1, 2, 3]]) + 1

    def predict(self, X: np.ndarray):
        """
        predict using the ensemble- each model gives prediction and then the major vote is calculated.
        :param X: data to preform prediction on
        :return: prediction by each ensemble in a np.array
        """
        X = self.selector.transform(X)
        ensemble_prediction = np.ndarray((len(self._ensemble), X.shape[0]))
        for i, current_classifier in enumerate(self._ensemble):
            ensemble_prediction[i] = current_classifier.predict(X)
        prediction = np.apply_along_axis(func1d=self._count_classes, axis=0, arr=ensemble_prediction)

        return prediction.reshape((prediction.shape[0], 1))

    ## not relevant to this classifier
    def update(self, X: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    def save_classifier(self):
        """
        save the current classifier to pickle.
        :return:  None
        """
        pickle.dump(self._ensemble, open(self._config.MODEL_PATH + "_Ensemble", 'wb'))

    def load_classifier(self):
        """
        load classifier from pickle.
        :return: None
        """
        self._ensemble = pickle.load(open(self._config.MODEL_PATH + "_Ensemble", 'rb'))

    def evaluate(self, X: np.ndarray, y: np.ndarray):
        """
        evaluation of the current model.
        :param X: data
        :param y: labels
        :return: None
        """
        # self.save_classifier() # uncomment if you want to save the current model
        prediction = self.predict(X)
        print("----------------------- EVALUATION --------------------------")
        x = classification_report(y, prediction)
        print(x)
        pickle.dump(self._ensemble, open(f"xgb_ensemble_{x['accuracy']}", 'wb'))