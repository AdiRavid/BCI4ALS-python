########################################################################################################################
#                                                      Imports                                                         #
########################################################################################################################
import mne
from threading import Thread
from typing import Union

from new_bci_framework.config.config import Config


########################################################################################################################
#                                                   Implementation                                                     #
########################################################################################################################
class Recorder:
    """
    Takes care of all aspects of recording the eeg data.
    Public API for starting and stopping a recording, for pushing markers if a recording is in progress and for
    retrieving the data from the last recording as mne.Raw.
    """
    def __init__(self, config: Config):
        self._config = config

    def start_recording(self) -> None:
        """
        Turn on recording device and start streaming.
        """
        raise NotImplementedError

    def end_recording(self) -> None:
        """
        Get data from stream and turn off recording device.
        """
        raise NotImplementedError

    def get_raw_data(self) -> mne.io.Raw:
        """
        Retrieve data from stream (and empty buffer) and transform to an mne object.
        :return: An mne Raw object storing the data from the recording.
        """
        raise NotImplementedError

    def get_partial_raw_data(self) -> mne.io.Raw:
        """
        Retrieve data from stream (from the last point retrieved, without emptying the buffer) and transform to an mne
        object.
        :return: An mne Raw object storing partial data from the recording.
        """
        raise NotImplementedError

    def push_marker(self, marker: int) -> None:
        """
        Inserts a marker to the recording device's stream.
        :param marker: An integer representing the prediction (should be in [1, len(config.CLASSES)]).
        """
        raise NotImplementedError

    def plot_live_data(self, block=True) -> Union[None, Thread]:
        """
        Plot the data being captured in real time.
        Call after recording started. Will block execution until plot is closed unless block is set to false.
        @:return If block is False, return a thread handle that must be joined before exit, else return None.
        """
        raise NotImplementedError
