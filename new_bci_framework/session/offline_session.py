import pickle

from new_bci_framework.classifier.sgd_classifier import SGDClassifier
from new_bci_framework.session.session import Session
from new_bci_framework.recorder.recorder import Recorder
from new_bci_framework.classifier.xgb_classifier import XGBClassifier
from new_bci_framework.classifier.adaboost_classifier import adaboost_classifier

from new_bci_framework.paradigm.paradigm import Paradigm
from new_bci_framework.preprocessing.preprocessing_pipeline import PreprocessingPipeline
from new_bci_framework.config.config import Config
import numpy as np
import pickle as pkl
import new_bci_framework.classifier.optuna_runner as op


from mne.io import read_raw_fif
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif, chi2, f_regression, \
    mutual_info_regression, SelectFpr


class OfflineSession(Session):
    """
    Subclass of session for an offline recording session.
    """

    def __init__(self, config: Config, recorder: Recorder, paradigm: Paradigm,
                 preprocessor: PreprocessingPipeline,
                 classifier: XGBClassifier = None, sgd_classifier: SGDClassifier = None,
                 adaboost_classifier: adaboost_classifier = None):
        super().__init__(config, recorder, paradigm,
                         preprocessor, classifier, sgd_classifier, adaboost_classifier)

    def run_recording(self, save=True):
        self.recorder.start_recording()
        self.recorder.plot_live_data()
        self.paradigm.start(self.recorder)
        self.recorder.end_recording()

        if save:
            self.raw_data = self.recorder.get_raw_data()
            self.raw_data.save(f'../data/{self.config.SUBJECT_NAME}_{self.config.DATE}_raw.fif')

    def run_preprocessing(self):
        self.epoched_data, self.epoched_labels = self.preprocessor.run_pipeline(self.raw_data)
        # self.preprocessor.run_pipeline(self.raw_data)

    # chose features
    # data is of size (n_epochs, n_features)
    # labels is of size n_epochs
    def feature_selection(self):
        num_of_features = self.config.NUM_OF_FEATURES

        X = self.epoched_data
        y = self.epoched_labels.ravel()
        if not self.config.SELECTED_FEATURES_PATH:
            selector = SelectKBest(score_func=mutual_info_classif, k=num_of_features)
            selector.fit(X, y)
            current_features_idxes = selector.get_support(indices=True)
            self.data_in_features = selector.fit_transform(X, y)
            pickle.dump(current_features_idxes, open("feature_selection", 'wb'))
        else:
            current_features_idxes = pickle.load(open(self.config.SELECTED_FEATURES_PATH, 'rb'))
            self.data_in_features = X[:, current_features_idxes]

        # self.data_in_features = SelectKBest(score_func=mutual_info_classif, k=num_of_features).fit_transform(X, y)

        # self.data_in_features = SelectKBest(score_func=f_classif, k=num_of_features).fit_transform(X, y)
        # self.data_in_features = SelectKBest(score_func=chi2, k=num_of_features).fit_transform(X, y) - cant use due to negative values
        # self.data_in_features = SelectKBest(score_func=f_regression, k=num_of_features).fit_transform(X, y)
        # self.data_in_features = SelectKBest(score_func=mutual_info_regression, k=num_of_features).fit_transform(X, y)



    def run_classifier(self):
        labels = self.epoched_labels  # .ravel()
        all_data = np.concatenate((labels, self.data_in_features), axis=1)
        train_data, test_data = train_test_split(all_data)
        # train_file = open('train_file.pkl', 'wb')
        # pkl.dump(train_data,train_file)
        # test_file = open('test_file.pkl', 'wb')
        # pkl.dump(test_data, test_file)

        # op.run_optuna(train_data[:, 1:], train_data[:, 0])

        if self.config.NEW_MODEL:
            self.classifier.fit(train_data)
        else:
            self.classifier.update(train_data)
        self.classifier.evaluate(test_data)

    def run_adaboost(self):
        labels = self.epoched_labels  # .ravel()
        all_data = np.concatenate((labels, self.data_in_features), axis=1)
        train_data, test_data = train_test_split(all_data)
        # op.run_optuna(train_data[:, 1:], train_data[:, 0])

        self.adaboost_classifier.fit(train_data)
        self.adaboost_classifier.evaluate(test_data)

    def run_sgd_classifier(self):
        labels = self.epoched_labels  # .ravel()
        all_data = np.concatenate((labels, self.data_in_features), axis=1)
        train_data, test_data = train_test_split(all_data)

        if self.config.NEW_MODEL:
            self.sgd_classifier.fit(train_data)
        else:
            self.sgd_classifier.update(train_data)
        evaluation = self.sgd_classifier.evaluate(test_data)

    # def run_lazy_classifier(self):
    #     labels = self.epoched_labels  # .ravel()
    #     all_data = np.concatenate((labels, self.data_in_features), axis=1)
    #     train_data, test_data = train_test_split(all_data)
    #     lazy_classifier = LazyClassifier(self.config)
    #     lazy_classifier.check_models(train_data)


    # if given raw_data it will do the pipeline on it
    # if no data were given it will evoke the recorder
    def run_all(self, raw_data_path=''):
        if not raw_data_path:
            self.run_recording()
            self.raw_data = self.recorder.get_raw_data()
        else:
            self.raw_data = read_raw_fif(raw_data_path, preload=True)
        self.run_preprocessing()
        self.feature_selection()
        #self.run_adaboost()
        self.run_classifier()
        #self.run_sgd_classifier()
        #self.run_lazy_classifier()
