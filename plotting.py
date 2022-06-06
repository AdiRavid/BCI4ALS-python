import mne
import tkinter

import numpy as np
import matplotlib

matplotlib.use('tkagg')
import matplotlib.pyplot as plt

plt.interactive(True)

raw = mne.io.read_raw_fif(r"C:\Users\ASUS\Desktop\BCI4ALS\data\Sivan\Sivan_2022-06-05-15-26_raw.fif", preload=True)

raw.plot()
raw.plot_psd()
plt.show(block=True)
