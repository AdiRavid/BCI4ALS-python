import mne
import numpy as np
import matplotlib.pyplot as plt

raw = mne.io.read_raw_fif(r"C:\Users\ASUS\Documents\BCI4ALS-python-new\data\Michael_11-4-22_raw.fif", preload=True)
raw2 = mne.io.read_raw_fif(r"C:\Users\ASUS\Documents\BCI4ALS-python-new\data\Synth_2022-04-18-20-57_raw.fif", preload=True)
raw.plot()
raw.plot_psd()