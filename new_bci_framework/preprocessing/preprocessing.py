import numpy as np

import mne
from new_bci_framework.config.config import Config


class PreprocessingPipeline:
    """
    A Preprocessing pipeline. In essence it receives a raw data object and returns the segmented data as
    an Epochs object, after preforming filters, cleaning etc.
    Further design of this class can allow subclassing or other forms of modularity, allowing us to easily
    swap different pipelines.
    """

    def __init__(self, config: Config):
        self.config = config
        pass

    def run_pipeline(self, data: mne.io.Raw) -> mne.Epochs:
        data = self.__add_annotations_from_stim(data)
        filtered_data = self._highpass_lowpass_filter((data))
        filtered_data = self._notch_filter(filtered_data)

    def __add_annotations_from_stim(self, data: mne.io.Raw) -> mne.io.Raw:
        """
        Raw objects contains a STIM channel indicating events.
        This method extracts the markers from this channels and adds them as annotations to the mne Raw object.
        """
        stim_ch_data = data.get_data('STIM')[0]
        event_times = np.nonzero(stim_ch_data)[0]
        event_vals = stim_ch_data[event_times]
        events = np.stack([event_times, np.zeros_like(event_times), event_vals], axis=1)
        annot_from_events = mne.annotations_from_events(
            events=events, event_desc=self.config.CLASSES, sfreq=data.info['sfreq'])
        data.set_annotations(annot_from_events)
        data.drop_channels('STIM')
        return data


    def _notch_filter(self, data: mne.io.Raw):
        data.notch_filter(freqs=50., filter_length=180)
        return data

    def _highpass_lowpass_filter(self, data: mne.io.Raw):
        data.filter(0.1, 60., fir_design='firwin', skip_by_annotation='edge')
        return data

    def clean_artifacts(self, data: mne.io.Raw):
        pass

    def ICA(self, data: mne.io.Raw):
        #TODO: update parameters:

        # refit the ICA with 30 components this time
        new_ica = ICA(n_components=30, max_iter='auto', random_state=97)
        new_ica.fit(filt_raw)

        # find which ICs match the ECG pattern
        ecg_indices, ecg_scores = new_ica.find_bads_ecg(raw, method='correlation',
                                                        threshold='auto')
        new_ica.exclude = ecg_indices

        # barplot of ICA component "ECG match" scores
        new_ica.plot_scores(ecg_scores)

        # plot diagnostics
        new_ica.plot_properties(raw, picks=ecg_indices)

        # plot ICs applied to raw data, with ECG matches highlighted
        new_ica.plot_sources(raw, show_scrollbars=False)

        # plot ICs applied to the averaged ECG epochs, with ECG matches highlighted
        new_ica.plot_sources(ecg_evoked)
