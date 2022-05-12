import os, mne
import numpy as np
from scipy.stats import zscore

matlab_annotations = {'LEFT': '1.000000000000000',
                      'RIGHT': '2.000000000000000',
                      'IDLE': '3.000000000000000'}

channels = np.array(['C3', 'C4', 'Cz', 'FC1', 'FC2', 'FC5', 'FC6', 'CP1', 'CP2', 'CP5', 'CP6'])
mapping = {**{o: n for o, n in zip(channels, np.roll(channels, 1))}, **{'STIM': 'STIM'}}

files = os.listdir(r'data')
files = [f for f in files if f.endswith('raw.fif') and f.startswith('Michael')]


montage = mne.channels.make_standard_montage('biosemi64')

raws = []
for f in files:
    raw = mne.io.read_raw_fif(os.path.join(r'data', f), preload=True)

    #raw.plot_psd()

    #####################################
    # Matlab fix
    #####################################
    if not f.startswith('Michael_2022'):
        raw.info['sfreq'] = 125
        events, _ = mne.events_from_annotations(raw, {'1.000000000000000': 1,
                                                      '2.000000000000000': 2,
                                                      '3.000000000000000': 3})
        stim = np.zeros_like(raw.get_data()[0])
        stim[events[:, 0]] = events[:, 2]
        stim_info = mne.create_info(['STIM'], raw.info['sfreq'], ['STIM'])
        stim_raw = mne.io.RawArray(stim.reshape(1, -1), stim_info)
        raw.add_channels([stim_raw], force_update_info=True)

    #####################################
    ## fixes for specific recording days
    #####################################
    if "2022-04-28" in f:
        raw.rename_channels(mapping)
        raw.reorder_channels(np.concatenate([channels, np.array(['STIM'])]))
        raw.info['bads'] = ['CP6']
        raw.drop_channels(raw.info['bads'])
        raw.info.set_montage(montage)


    if "2022-05-08" in f:
        raw.rename_channels({'stim': 'STIM'})

    #####################################
    # normalization
    #####################################
    L = raw.get_data()[:-1]
    raw._data[:-1] = L/np.linalg.norm(L)
    #raw._data[:-1] = zscore(L)
    #####################################

    #raw.plot_psd()

    raws.append(raw)
    try:
        raw.save(os.path.join(r'data', f.split('.')[0] + '_normed_no_cp6.fif'))
        break
    except FileExistsError:
        continue


print()
#raw = mne.concatenate_raws(raws)
#raw.save(os.path.join(r'data', 'all_data_12_05_22_normed.fif'))
