import mne

from ..config.config import Config


class PreprocessingPipeline:
    """
    A Preprocessing pipeline. In essence it receives a raw data object and returns teh segmented data as
    an Epochs object, after preforming filters, cleaning etc.
    Further design of this class can allow subclassing or other forms of modularity, allowing us to easily
    swap different pipelines.
    """

    def __init__(self, config: Config):
        pass

    def run_pipeline(self, data: mne.io.Raw) -> mne.Epochs:
        pass
