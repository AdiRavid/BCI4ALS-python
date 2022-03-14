from threading import Thread
from typing import Union

import mne
from ..config.config import Config


class Recorder:
    """
    Take care of all aspects of recording the eeg data. If any other program need to be opened manually
     then this class should prompt the user to do that.
     public API for starting and stopping a recording, for pushing markers if a recording is in progress and
      for retrieving the data from the last recording as mne.Raw.
    """

    def __init__(self, config: Config):
        pass

    def start_recording(self):
        pass

    def push_marker(self, marker: float):
        pass

    def end_recording(self):
        pass

    def get_raw_data(self) -> mne.io.Raw:
        pass

    def plot_live_data(self, block=True) -> Union[None, Thread]:
        """
        Plot the data being captured in real time.
        Call after recording started.
        Will block execution until plot is closed unless block is set to false.
        if block is false, return a thread handle that must be joined before exit
        """
        pass
