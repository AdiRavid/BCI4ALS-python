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
        pass

    def run_pipeline(self, data: mne.io.Raw) -> mne.Epochs:
        filtered_data = self._highpass_lowpass_filter((data))
        filtered_data = self._notch_filter(filtered_data)

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
