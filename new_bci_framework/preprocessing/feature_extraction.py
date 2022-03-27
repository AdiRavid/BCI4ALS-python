import mne
import numpy as np
from mne.datasets import sample
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, KFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from mne_features.feature_extraction import extract_features

labels = []  # TODO: add labels from Adi.

bands_mat = [[15.5, 18.5],
             [8, 10.5],
             [10, 15.5],
             [17.5, 20.5],
             [12.5, 30]]

sfreq = 0  # TODO add freqs from raw data or from config.

highpass = 60  # TODO from config

lowpass = 60  # TODO from config


def feature_extraction(epochs: mne.Epochs):
    data = epochs.get_data()
    pipe = Pipeline()  # TODO: add classifiers.
    y = labels

    selected_funcs = {'pow_freq_bands', 'rms', 'spect_edge_freq',
                      'spect_entropy', 'spect_slope',
                      'mean', 'variance', 'std', 'skewness', 'ptp_amp',
                      'hjorth_mobility', 'hjorth_complexity'}
    func_params = {'pow_freq_bands__freq_bands': np.asarray(bands_mat),
                   'spect_entropy__sfreq': sfreq,
                   'spect_slope__sfreq': sfreq,
                   'spect_slope__fmax': highpass,
                   'spect_slope__fmin': lowpass,
                   'spect_edge_freq__sfreq': sfreq,
                   }
    X_new = extract_features(data, sfreq, selected_funcs, func_params)
    kf = KFold(n_splits=3, shuffle=True, random_state=42)
    scores = cross_val_score(pipe, X_new, y, scoring='accuracy', cv=kf)
    print(scores)
