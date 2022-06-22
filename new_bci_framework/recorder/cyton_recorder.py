########################################################################################################################
#                                                      Imports                                                         #
########################################################################################################################
import threading
from typing import Optional, List, Union
from nptyping import NDArray

from os.path import isfile
import serial.tools.list_ports
import mne
from mne.io import RawArray
from brainflow import BrainFlowInputParams, BoardShim, BoardIds

from new_bci_framework.config.config import Config
from new_bci_framework.recorder.recorder import Recorder
from new_bci_framework.recorder.plot_rt_recording import Graph


########################################################################################################################
#                                                   Implementation                                                     #
########################################################################################################################
class CytonRecorder(Recorder):
    """
    A subclass of :class:`Recorder` which implements recording via a Cyton board.
    """
    def __init__(self, config: Config, board_id: int = BoardIds.CYTON_DAISY_BOARD.value, ip_port: int = 6677,
                 serial_port: Optional[str] = None, headset: str = "cyton"):
        super(CytonRecorder, self).__init__(config)

        # Board Id and Headset Name
        self.headset: str = headset
        self.board_id = board_id
        self.channels = self._config.CHANNELS
        self.empty_channel_prefix = config.EMPTY_CHANNEL_PREF
        self.MONTAGE_FILENAME = config.MONTAGE_FILENAME

        # synthetic headset name
        if board_id == BoardIds.SYNTHETIC_BOARD:
            self.headset = 'synth'

        # BrainFlowInputParams
        self.params = BrainFlowInputParams()
        self.params.ip_port = ip_port
        self.params.serial_port = serial_port if serial_port is not None else self.__find_serial_port()
        self.params.headset = headset
        self.params.board_id = board_id
        self.board = BoardShim(board_id, self.params)

        # Other Params
        self.sfreq = self.board.get_sampling_rate(board_id)
        self.marker_row = self.board.get_marker_channel(self.board_id)
        self.ch_names = self.__get_board_names(self.channels)
        self.data = None

        self.buffer_size = 0

    def start_recording(self) -> None:
        """
        see :func:'start_recording <new_bci_framework.recorder.recorder.Recorder.start_recording>'
        """
        self.board.prepare_session()
        if self._config.GAIN_VALUE:
            self.board.config_board(self._config.HARDWARE_GAIN_MSG)
        self.board.start_stream()

    def end_recording(self) -> None:
        """
        see :func:'end_recording <new_bci_framework.recorder.recorder.Recorder.end_recording>'
        """
        self.data = self.board.get_board_data()
        self.board.stop_stream()
        self.board.release_session()

    def push_marker(self, marker) -> None:
        """
        see :func:'push_marker <new_bci_framework.recorder.recorder.Recorder.push_marker>'
        """
        self.board.insert_marker(marker)  # insert the marker to the stream

    def get_raw_data(self) -> RawArray:
        """
        see :func:'get_raw_data <new_bci_framework.recorder.recorder.Recorder.get_raw_data>'
        """
        return self.__get_raw_data(self.ch_names)

    def get_partial_raw_data(self) -> RawArray:
        """
        see :func:'get_partial_raw_data <new_bci_framework.recorder.recorder.Recorder.get_partial_raw_data>'
        """
        buffer_size = self.board.get_board_data_count()
        self.data = self.board.get_current_board_data(buffer_size - self.buffer_size)
        self.buffer_size = buffer_size
        return self.__get_raw_data(self.ch_names)

    def plot_live_data(self, block=True) -> Union[None, threading.Thread]:
        """
        see :func:'plot_live_data <new_bci_framework.recorder.recorder.Recorder.plot_live_data>'
        """
        start_plot = lambda: Graph(self.board, self.__get_board_names(self.channels), self._config)
        if block:
            start_plot()
        else:
            thread = threading.Thread(target=start_plot)
            thread.start()
            return thread

    def __get_board_names(self, channels: Optional[List[str]]) -> List[str]:
        """
        Gets the names of the channels from the board, if not provided explicitly.
        :param channels: A list of channel names, if known and provided, otherwise None.
        :return: The board's channel names.
        """
        if channels:
            return channels
        else:
            return self.board.get_eeg_names(self.board_id)

    def __find_serial_port(self) -> str:
        """
        @:return The string of the serial port to which the FTDI dongle is connected (e.g. return "COM5").
        If running in Synthetic mode, return "".
        """
        if self.board_id == BoardIds.SYNTHETIC_BOARD:
            return ""
        else:
            plist = serial.tools.list_ports.comports()
            FTDIlist = [comport for comport in plist if comport.manufacturer == 'FTDI']
            if len(FTDIlist) > 1:
                raise LookupError(
                    "More than one FTDI-manufactured device is connected. Please enter serial_port manually.")
            if len(FTDIlist) < 1:
                raise LookupError("FTDI-manufactured device not found. Please check the dongle is connected")
            return FTDIlist[0].device

    def __get_raw_data(self, ch_names: List[str]) -> mne.io.RawArray:
        """
        Subsets the data from the board's stream to 2 ndarrays: data - relevant eeg channels and stim - the channel
        where trial markers were kept.
        Notice that channel count start from 1 so eeg channel indices need to be fixed.
        Arrays are than given to :func:'<new_bci_framework.recorder.cyton_recorder.CytonRecorder.__board_to_mne>'
        which returns a Raw mne object.
        :param ch_names: list[str] of channels to select.
        :return: An mne Raw object storing the data from the recording.
        """
        ch_names = [ch_name for ch_name in ch_names if not ch_name.startswith(self.empty_channel_prefix)]
        indices = [self.ch_names.index(ch) + 1 for ch in ch_names]
        stim = self.data[self.board.get_marker_channel(self.board_id)]
        data = self.data[indices]
        return self.__board_to_mne(data, stim, ch_names)

    def __board_to_mne(self, eeg_data: NDArray, stim: NDArray, ch_names: List[str]) -> mne.io.RawArray:
        """
        Convert the ndarrays of eeg and stim data to an mne object.
        :param eeg_data: ndarray of raw data from board.
        :param stim: ndarray of the stimuli markers aligned to the time they were shown in the recording.
        :param ch_names: list[str] of channels to select.
        :return: an mne Raw object storing the data from the recording.
        """
        eeg_data = eeg_data / 1e6  # BrainFlow returns uV, convert to V for MNE
        if self.board_id == BoardIds.CYTON_DAISY_BOARD:
            # rescale if gain value is not 24:
            eeg_data *= (
                    24 // self._config.GAIN_VALUE)

        # Creating MNE objects from BrainFlow data arrays
        ch_types = ['eeg'] * len(ch_names)
        info = mne.create_info(ch_names=ch_names, sfreq=self.sfreq, ch_types=ch_types)

        if isfile(self._config.MONTAGE_FILENAME):
            montage = mne.channels.read_custom_montage(fname=self._config.MONTAGE_FILENAME)
        else:
            montage = mne.channels.make_standard_montage('biosemi64')
        info.set_montage(montage)
        raw = mne.io.RawArray(eeg_data, info, verbose=False)

        # Add marker channel:
        marker_info = mne.create_info(ch_names=['stim'], sfreq=self.sfreq, ch_types=['stim'])
        marker_raw = mne.io.RawArray([stim], marker_info)

        raw.add_channels([marker_raw])
        return raw
