from os import listdir
from pyxdf import resolve_streams, match_streaminfos
from mnelab.io.xdf import read_raw_xdf
import mne
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate, cross_val_predict
from sklearn.decomposition import PCA
from mne.decoding import (CSP, FilterEstimator, UnsupervisedSpatialFilter,
                          cross_val_multiscore)

from scipy.io import loadmat

START_REC = '0.000000000000000'
END_REC = '99.00000000000000'
BASELINE = '1001.000000000000'
START_TRIAL = '1111.000000000000'
LEFT = '1.000000000000000'
RIGHT = '2.000000000000000'
IDLE = '3.000000000000000'
END_TRIAL = '9.000000000000000'

ALL_EVENTS = np.array(sorted([START_REC, END_REC, BASELINE, START_TRIAL,
                              LEFT, RIGHT, IDLE, END_TRIAL]))
EVENT_DICT = {ALL_EVENTS[i]: i for i in range(len(ALL_EVENTS))}

EVENT_NAMES = {LEFT: 'left', RIGHT: 'right', IDLE: 'idle'}

CHANNELS = ['C3', 'C4', 'Cz',
                         'FC1', 'FC2', 'FC5', 'FC6',
                         'CP1', 'CP2', 'CP5', 'CP6']
CHANNELS = {str(i): channel for i, channel in enumerate(CHANNELS)}

PATH = r'C:\Users\ASUS\Documents\BCI4ALS-python-new\data\xdf_files' #TODO: path that contains XDF files.


f = [f'{PATH}\{f}' for f in listdir(PATH) if f.split('.')[-1] == 'xdf'][0]
stream_info = resolve_streams(f)
eeg_stream = match_streaminfos(stream_info, [{'type': 'EEG'}])[0]
raw = read_raw_xdf(f, stream_id=eeg_stream)

raw.drop_channels(raw.info["ch_names"][11:])
raw.rename_channels(CHANNELS)
raw.set_montage("easycap-M1")

SUBJECT_NAME = "Michael"
DATE = "11-4-22"
PATH = r"C:\Users\ASUS\Documents\BCI4ALS-python-new\data"
raw.save(f"{PATH}\{SUBJECT_NAME}_{DATE}_raw.fif")


# raw.filter(l_freq=0.5, h_freq=40)
# raw.notch_filter(50)
#
#
# events, _ = mne.events_from_annotations(raw, EVENT_DICT)
#
# event_dict = {val: EVENT_DICT[key] for key, val in EVENT_NAMES.items()}
# events = events[np.in1d(events[:, 2], list(event_dict.values())), :]
#
# tmin, tmax = -2, 8
# epochs = mne.Epochs(raw, events, event_dict, tmin, tmax, baseline=None, preload=True)
#
# X = epochs.get_data()
# y = epochs.events[:, 2]
#
# clf = make_pipeline(
#     FilterEstimator(epochs.info, 0.5, 45),
#     CSP(),
#     RandomForestClassifier(n_estimators=200)
# )
#
#
# scores = cross_val_multiscore(clf, X, y, cv=10)
#
# print()
