import mne
import numpy as np
import matplotlib.pyplot as plt

raw = mne.io.read_raw_fif(r"C:\Users\Sivan\PycharmProjects\BCI\BCI4ALS-python\data\Michael_2022-04-28-17-46_raw.fif", preload=True)
raw = raw.drop_channels('STIM')
#raw2 = mne.io.read_raw_fif(r"C:\Users\ASUS\Documents\BCI4ALS-python-new\data\Synth_2022-04-18-20-57_raw.fif", preload=True)
raw.plot()
raw.plot_psd()