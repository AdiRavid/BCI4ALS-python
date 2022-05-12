import os
from mne.io import read_raw_fif

# plot raw data and spectogram
search_path = os.path.join(os.getcwd(), "../..")
raws = []
for root, dir, files in os.walk(search_path):
    for file in files:
        if file.endswith(".fif"):
            file_full_path = os.path.join(root, file)
            raw = read_raw_fif(file_full_path, preload=True)
            if "2022-04-28" in file_full_path:
                raw.drop_channels('STIM')
                raw.drop_channels('C3')

            raw.plot()
            raw.plot_psd()





