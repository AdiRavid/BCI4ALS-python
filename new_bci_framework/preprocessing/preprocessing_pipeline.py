import os
from typing import Dict, Tuple

import mne
import numpy as np
import pandas

from ..config.config import Config
from mne_features.feature_extraction import extract_features
from new_bci_framework.config.config import Config
from autoreject import AutoReject


class PreprocessingPipeline:
    """
    A Preprocessing pipeline. In essence it receives a raw data object and returns teh segmented data as
    an Epochs object, after preforming filters, cleaning etc.
    Further design of this class can allow subclassing or other forms of modularity, allowing us to easily
    swap different pipelines.
    """

    def __init__(self, config: Config):
        self._config = config
        self._save_dir = f"{self._config.SESSION_SAVE_DIR}/preprocessor"
        if not os.path.isdir(self._save_dir):
            os.mkdir(self._save_dir)

    def _segment(self, data: mne.io.Raw) -> mne.Epochs:
        event_dict: Dict[str, int] = {v: k for k, v in self._config.TRIAL_LABELS.items()}
        events = mne.find_events(data)

        epochs = mne.Epochs(data,
                            events,
                            tmin=self._config.TRIAL_START_TIME,
                            tmax=self._config.TRIAL_END_TIME,
                            event_id=self._config.TRIAL_LABELS,
                            verbose='INFO',
                            on_missing='warn', preload=True)
        epochs.drop_channels('stim')
        self.epochs = epochs
        return epochs

    def __feature_extraction(self, raw_data: mne.io.Raw):
        bands_mat = [[15.5, 18.5],
                     [8, 10.5],
                     [10, 15.5],
                     [17.5, 20.5],
                     [12.5, 30],
                     [30,40],
                     [40,45]] #check which frequencies are relevant

        sfreq = raw_data.info['sfreq']

        highpass = self._config.HIGH_PASS_FILTER
        lowpass = self._config.LOW_PASS_FILTER

        data_channels = self.epochs.ch_names[0:-1] #remove 'STIM' channel
        data = self.epochs.get_data(data_channels)

        # feature documentation:
        # https://mne.tools/mne-features/api.html
        selected_funcs = {'pow_freq_bands', 'rms',
                          'spect_edge_freq',
                          'spect_entropy',
                          'spect_slope',
                          'mean', 'variance', 'std', 'skewness', 'ptp_amp',
                          'hjorth_mobility', 'hjorth_complexity'}
        func_params = {'pow_freq_bands__freq_bands': np.asarray(bands_mat),
                       'spect_slope__fmax': lowpass,
                       'spect_slope__fmin': highpass,
                       }
        features_df = extract_features(data, sfreq, selected_funcs, funcs_params=func_params, return_as_df=True)
        self.epoched_data = features_df.to_numpy()

        # save features list
        filename = raw_data.filenames[0].split('/')[-1].split('.')[0]
        features_df.to_excel(os.path.join("new_bci_framework","preprocessing", filename + "_" + "all_features.xlsx"))

        self.epoched_labels = np.asarray(self.epochs.events[:,2])
        self.epoched_labels = np.reshape(self.epoched_labels,(self.epoched_labels.shape[0],1))
        # np.reshape(self.epoched_labels, self.epoched_labels.shape[0])
        return self.epoched_data, self.epoched_labels

    def _filter(self, data: mne.io.Raw) -> None:
        ## 1. Lowpass highpass filter
        data.filter(l_freq=self._config.HIGH_PASS_FILTER, h_freq=self._config.LOW_PASS_FILTER)
        ## 2. Notch filter
        if self._config.NOTCH_FILTER:
            data.notch_filter(self._config.NOTCH_FILTER)

        ## 3. laplacian
        data = mne.preprocessing.compute_current_source_density(data)

    #rejects bad epochs according to the algorithm: https://autoreject.github.io/stable/explanation.html
    def _reject(self, data: mne.io.Raw):
        ar = AutoReject()
        epochs_clean, rejection_log = ar.fit_transform(self.epochs, True)
        self.epochs = epochs_clean

    def run_pipeline(self, data: mne.io.Raw) -> Tuple[np.ndarray, np.ndarray]:
        self._filter(data)
        self._segment(data)
        self._reject(data)
        return self.__feature_extraction(data)
