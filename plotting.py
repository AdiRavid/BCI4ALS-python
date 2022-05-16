import mne
import numpy as np
import matplotlib.pyplot as plt
import os

search_path = os.path.join(os.getcwd(), "..")

raw = mne.io.read_raw_fif(r"C:\Users\Sivan\PycharmProjects\BCI\BCI4ALS-python\data\Michael_2022-05-15-18-45_raw.fif", preload=True)
# raw = raw.drop_channels('CP6')
# mne.rename_channels(raw.info,{'stim':'STIM'})
# raws = []
# raws.append(raw)
# raw2 = mne.io.read_raw_fif(r"C:\Users\Sivan\PycharmProjects\BCI\BCI4ALS-python\data\all_data_up_to_may1_normed_no_CP6.fif", preload=True)
# raws.append(raw2)
# concated_raw = mne.concatenate_raws(raws)
# concated_raw.save("C:\\Users\\Sivan\\PycharmProjects\\BCI\\BCI4ALS-python\\data\\all_files_until_09-05_no_CP6.fif")
# #raw2 = mne.io.read_raw_fif(r"C:\Users\ASUS\Documents\BCI4ALS-python-new\data\Synth_2022-04-18-20-57_raw.fif", preload=True)
raw.plot()
raw.plot_psd()