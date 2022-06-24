import os
import pickle
import random

from mne.io import read_raw_fif

from new_bci_framework.session.session import Session
from new_bci_framework.config.config import Config
from new_bci_framework.recorder.recorder import Recorder
from new_bci_framework.ui.recording_ui.recording_ui import RecordingUI
from new_bci_framework.paradigm.paradigm import Paradigm
from new_bci_framework.preprocessing.preprocessing_pipeline import PreprocessingPipeline
from new_bci_framework.classifier.base_classifier import BaseClassifier

import numpy as np
from sklearn.model_selection import train_test_split


class OfflineSession(Session):
    """
    Subclass of session for an offline recording session.
    """

    def __init__(self, config: Config, recorder: Recorder, ui: RecordingUI, paradigm: Paradigm,
                 preprocessor: PreprocessingPipeline, classifier: BaseClassifier):
        """
        init a session
        :param config: config object for the session
        :param recorder: recorder object for the session
        :param ui: ui object for the session
        :param paradigm: paradigm object for the session
        :param preprocessor: preprocessor object for the session
        :param classifier: classifier object for the session
        """
        super().__init__(config, recorder, ui, paradigm, preprocessor, classifier)
        self.save = True

    def run_paradigm(self):
        """
        run paradigm in length of events, using the ui object.
        :return: None
        """
        events = self.paradigm.get_events()
        work = len(events)
        self.ui.set_work(work)

        self.ui.setup()
        for i in range(work):
            if self.ui.need_to_quit():
                break
            self.ui.set_curr_work(i)
            self.ui.clear_surface(self.ui.screen)
            self.ui.display_event(self.recorder, events[i], self.ui.screen)
        self.ui.quit()


    def run_classifier(self, split=True):
        """
        fit the classifier with data from current session. if split is true, split the data to train and test.
        train the model with the train test and evaluate on the test set. otherwise, train the model on all of the data.
        :param split:
        :return:
        """
        if split:
            X_train, X_test, y_train, y_test = train_test_split(self.processed_data, self.labels, stratify=self.labels)
            self.classifier.fit(X_train, y_train)
            self.run_evaluation(X_test, y_test)
        else:
            X_train, y_train = self.processed_data, self.labels
            self.classifier.fit(X_train, y_train)


    def run_evaluation(self, X_test, y_test):
        """
        run evaluation of the model on the given data.
        :param X_test: data
        :param y_test: labels
        :return: None
        """
        self.classifier.evaluate(X_test, y_test)
        pickle.dump(self.classifier, open("new_bci_framework/classifier/cur_classifier.sav", 'wb'))


    def run_all_without_classifier(self, raw_data_path=''):
        """
        run session without the classifier phase.
        if a path is given- use the data from the path.otherwise, record new data using the recorder.
        :param raw_data_path: path to raw_data
        :return: None
        """
        if not raw_data_path:
            self.run_recording()
            self.raw_data = self.recorder.get_raw_data()
        else:
            self.raw_data = read_raw_fif(raw_data_path, preload=True)

        self.filename = self.raw_data.filenames[0].split('/')[-1].split('.')[0]
        self.run_preprocessing()
        self.run_evaluation(self.processed_data, self.labels)

    def run_all_for_ensammble(self, raw_data_path):
        """
        run pipeline for the ensamble classifier. for each file the classifier train a seperate model.
        :param raw_data_path: path that contains all the files file
        :return: None
        """
        self.raw_data = read_raw_fif(raw_data_path, preload=True)

        self.filename = self.raw_data.filenames[0].split('/')[-1].split('.')[0]
        self.run_preprocessing()
        self.run_classifier(split=False)  # for ensemble don't use split.

    def run_all(self, raw_data_path=''):
        """
        run pipeline of a session. if raw_data_path is empty, the session will include only recording and
        saving the data. if raw_data_path is not empty, it should be a path for all data files (as .fif).
        this function do preprocess and segmantaion for each file on its own, and then concat all files
        (exlude the last file- save for test). after concat all files it runs the classifier (with split=true),
        and also make evaluation on the last file of data.

        :param raw_data_path: path to raw data
        :return: None
        """
        concat_epochs = None
        if not raw_data_path:  # recording without preprocess and classifier.
            self.run_recording()
            self.raw_data = self.recorder.get_raw_data()
        else:
            concat_process_data, concat_label = None, None
            files = (list(filter(lambda f: f.endswith(".fif"), os.listdir(os.path.join(os.getcwd(), raw_data_path)))))
            random.shuffle(files)
            for idx, f in enumerate(files[:-1]):
                print(f"<--- start preprocess for file {idx}: {f}--->")
                raw_path = os.path.join(os.getcwd(), raw_data_path, f)
                self.raw_data = read_raw_fif(raw_path, preload=True)

                self.filename = self.raw_data.filenames[0].split('/')[-1].split('.')[0]
                self.run_preprocessing()
                if idx == 0:
                    concat_process_data, concat_label = self.processed_data, self.labels
                    concat_epochs = self.preprocessor.epochs.get_data()
                else:
                    concat_process_data = np.concatenate((concat_process_data, self.processed_data), axis=0)
                    concat_label = np.concatenate((concat_label, self.labels), axis=0)
                    concat_epochs = np.concatenate((concat_epochs, self.preprocessor.epochs.get_data()), axis=0)

            print(f"<--- Done preprocess- concat and start fit classifier--->")

            self.processed_data, self.labels = concat_process_data, concat_label
            self.run_classifier(split=True)

            # evaluate for last file
            raw_path_eval = os.path.join(os.getcwd(), raw_data_path, files[-1])
            print(f"<--- Done classifier, start evaluate with file {files[-1]}--->")
            self.raw_data = read_raw_fif(raw_path_eval, preload=True)
            self.filename = self.raw_data.filenames[0].split('/')[-1].split('.')[0]
            self.run_preprocessing()
            self.run_evaluation(self.processed_data, self.labels)

            concat_label = np.concatenate((concat_label, self.labels), axis=0)
            concat_epochs = np.concatenate((concat_epochs, self.preprocessor.epochs.get_data()), axis=0)

            ## uncomment if you want to save to pickle the concated data as ephochs and labels:
            # pickle.dump(concat_label, open("concat_label", 'wb'))
            # pickle.dump(concat_epochs, open("concat_epochs", 'wb'))