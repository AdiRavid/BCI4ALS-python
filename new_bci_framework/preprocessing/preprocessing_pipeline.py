import os
from typing import Optional, Tuple

import mne
import numpy as np

from mne_features.feature_extraction import extract_features
from new_bci_framework.config.config import Config
from autoreject import AutoReject

class PreprocessingPipeline:
    """
    A Preprocessing pipeline. In essence it receives a raw data object and returns teh segmented data as
    an np_array with another labels array composed of each feature for each epoch of data, ready to feed to the
    classifier.
    See run_pipeline for a thorough explanation of the preprocessing steps.
    Further design of this class can allow subclassing or other forms of modularity, allowing us to easily
    swap different pipelines.
    """

    def __init__(self, config: Config):
        self._config = config
        self._save_dir = f"{self._config.SESSION_SAVE_DIR}/preprocessor"
        if not os.path.isdir(self._save_dir):
            os.mkdir(self._save_dir)

        self.epochs: Optional[mne.Epochs] = None

    def _filter(self, raw: mne.io.Raw) -> Tuple[mne.io.Raw, np.ndarray]:
        events = mne.find_events(raw)
        raw = raw.drop_channels('stim')

        # 1. Lowpass highpass filter
        raw = raw.filter(l_freq=self._config.HIGH_PASS_FILTER, h_freq=self._config.LOW_PASS_FILTER, picks='eeg')
        # 2. Notch filter
        if self._config.NOTCH_FILTER:
            raw = raw.notch_filter(self._config.NOTCH_FILTER, picks='eeg')
        return raw, events

    def _segment(self, raw: mne.io.Raw, events: np.ndarray) -> mne.Epochs:
        epochs = mne.Epochs(raw,
                            events,
                            tmin=self._config.TRIAL_START_TIME,
                            tmax=self._config.TRIAL_END_TIME,
                            event_id=self._config.LABELS2MARKERS,
                            verbose='INFO', baseline=None,
                            on_missing='warn', preload=True)
        self.epochs = epochs
        return epochs

    def _reject(self):
        """
        rejects bad epochs according to the algorithm: https://autoreject.github.io/stable/explanation.html
        and runs ica on good epochs after to fix artifacts.
        """
        ar = AutoReject(verbose=True)
        epochs_clean, reject_log = ar.fit_transform(self.epochs, True)

        # run ica on good epochs
        ica = mne.preprocessing.ICA(random_state=99)
        ica.fit(epochs_clean)
        epochs_ica = ica.apply(self.epochs, exclude=ica.exclude)

        # exclude blinks and saccades
        exclude = [0,  # blinks
                   2]  # saccades

        # uncomment for plotting ica components
        #ica.plot_components(exclude)
        #ica.exclude = exclude

        self.epochs = epochs_ica

    def __baseline_correction(self):
        self.epochs = self.epochs.apply_baseline(baseline=(None, None), verbose=True)

    def __feature_extraction(self, raw):
        highpass = self._config.HIGH_PASS_FILTER
        lowpass = self._config.LOW_PASS_FILTER

        bands_mat = [[15.5, 18.5],
                     [8, 10.5],
                     [10, 15.5],
                     [17.5, 20.5],
                     [12.5, 30],
                     [30, 40],
                     [40, 45]]  # check which frequencies are relevant


        # feature documentation - https://mne.tools/mne-features/api.html
        # amplitude related features (rms,mean,std,skewness,ptp_amp) were commented out when working
        # with combined data from multiple session due to variability in amplitudes across sessions.
        selected_funcs = {'pow_freq_bands', #'rms',
                          'spect_edge_freq',
                          'spect_entropy',
                          'spect_slope', 'variance',
                          #'mean','std', 'skewness', 'ptp_amp',
                          'hjorth_mobility', 'hjorth_complexity'
                          }
        func_params = {'pow_freq_bands__freq_bands': np.asarray(bands_mat),
                       'spect_slope__fmax': lowpass,
                       'spect_slope__fmin': highpass
                       }

        processed_data_df = extract_features(self.epochs.get_data(), self.epochs.info['sfreq'],
                                             selected_funcs, funcs_params=func_params,
                                             return_as_df=True)
        self.processed_data = processed_data_df.to_numpy()

        # save features list
        filename = raw.filenames[0].split('/')[-1].split('.')[0]
        processed_data_df.to_excel(os.path.join("new_bci_framework", "preprocessing", filename + "_" + "all_features.xlsx"))

        self.labels = np.asarray(self.epochs.events[:, 2])
        return self.processed_data, self.labels



    def run_pipeline(self, raw: mne.io.Raw) -> Tuple[np.ndarray, np.ndarray]:
        # 1. highpass-lowpass & notch filter:
        raw, events = self._filter(raw)

        # 2. extract segments according to the events
        self.epochs = self._segment(raw, events)

        # 3. reject bad epochs and fix artifacts with ica
        #   (there is only one epoch during online session so we don't want to reject)
        if len(self.epochs) > 1:
            self._reject()

        # 4. baseline correction (needs to be after autoreject)
        self.__baseline_correction()

        # 5. Laplacian:
        self.epochs = mne.preprocessing.compute_current_source_density(self.epochs)

        # 6. Extract all features from each epoch
        #    returns data_in_features,labels to feed the classifier
        return self.__feature_extraction(raw)
