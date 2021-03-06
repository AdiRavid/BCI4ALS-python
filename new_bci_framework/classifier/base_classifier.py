import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import pickle
from os import path
import seaborn as sn
import matplotlib.pyplot as plt
from new_bci_framework.config.config import Config
from sklearn.feature_selection import SelectKBest, mutual_info_classif, f_classif, chi2, f_regression
import pandas as pd


class BaseClassifier:
    """
    Basic class for a classifier for session eeg data.
    API includes training, prediction and evaluation.
    """

    def __init__(self, config: Config):
        self._config = config
        self._model = None
        self.selector = None

    def feature_selection(self, X, y):
        """
        select features from given data, using Select K best.
        save the selected features to csv for documentation.
        """
        num_of_features = self._config.NUM_OF_FEATURES
        self.selector = SelectKBest(score_func=mutual_info_classif, k=num_of_features)
        res = self.selector.fit_transform(X, y)
        indices = self.selector.get_support(indices=True)
        df = pd.DataFrame(indices)
        df.to_csv('feature_selection.csv', index=False)

        return res

    def save_features(self):
        """
        save the selected feature to pickle.
        """
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
        """
        evaluate the model with the given data.
        print to console the result and create plot of confusion matrix.
        """
        self.save_classifier()
        prediction = self.predict(X)
        print("----------------------- EVALUATION --------------------------")
        print(classification_report(y, prediction))

        from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
        cmp = ConfusionMatrixDisplay(
            confusion_matrix(y, prediction),
            display_labels=['LEFT', 'IDLE', 'RIGHT'],
        )
        cmp.plot()
        plt.show()

    def save_classifier(self):
        raise NotImplementedError

    def load_classifier(self):
        raise NotImplementedError