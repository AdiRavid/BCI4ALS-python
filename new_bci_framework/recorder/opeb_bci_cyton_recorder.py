import atexit
import threading
import numpy as np
from typing import Optional, List, Union
from nptyping import NDArray

import mne
from mne.io import RawArray
import serial.tools.list_ports
from brainflow import BrainFlowInputParams, BoardShim, BoardIds

from new_bci_framework.recorder.plot_rt_recording import Graph
from new_bci_framework.recorder.recorder import Recorder

from new_bci_framework.config.config import Config

HARDWARE_SETTINGS_MSG_6 = "x1030110Xx2030110Xx3030110Xx4030110Xx5030110Xx6030110Xx7030110Xx8030110XxQ030110XxW030110XxE030110XxR030110XxT030110XxY131000XxU131000XxI131000X "
HARDWARE_SETTINGS_MSG_4 = "x1020110Xx2020110Xx3020110Xx4020110Xx5020110Xx6020110Xx7020110Xx8020110XxQ020110XxW020110XxE020110XxR020110XxT020110XxY121000XxU121000XxI121000X "



class CytonRecorder(Recorder):

    def __init__(self, config: Config,
                 board_id: int = BoardIds.CYTON_DAISY_BOARD.value,
                 ip_port: int = 6677,
                 serial_port: Optional[str] = None,
                 headset: str = "cyton"):
        super(CytonRecorder, self).__init__(config)

        # Board Id and Headset Name
        self.headset: str = headset
        self.board_id = board_id
        self.channels = config.CHANNELS
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

    def start_recording(self):
        super().start_recording()
        self.__on()

    def push_marker(self, marker):
        self.__insert_marker(marker)

    def end_recording(self):
        super().end_recording()
        self.__off()

    def get_raw_data(self) -> RawArray:
        return self.__get_raw_data(self.ch_names)

    def plot_live_data(self, block=True) -> Union[None, threading.Thread]:
        start_plot = lambda: Graph(self.board, self.__get_board_names(self.channels))
        if block:
            start_plot()
        else:
            thread = threading.Thread(target=start_plot)
            thread.start()
            return thread

    def __find_serial_port(self) -> str:
        """
        Return the string of the serial port to which the FTDI dongle is connected.
        If running in Synthetic mode, return ""
        Example: return "COM5"
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

    def __get_board_names(self, channels: List[str]) -> List[str]:
        """The method returns the board's channels"""
        if channels:
            return channels
        else:
            return self.board.get_eeg_names(self.board_id)

    def __on(self):
        """Turn EEG On"""
        self.board.prepare_session()
        self.board.config_board(HARDWARE_SETTINGS_MSG_4)
        self.board.start_stream()

    def __off(self):
        """Turn EEG Off"""
        self.data = self.__get_board_data()
        self.board.stop_stream()
        self.board.release_session()

    def __insert_marker(self, marker: float):
        """Insert an encoded marker into EEG data"""
        self.board.insert_marker(marker)  # insert the marker to the stream

    def __board_to_mne(self, board_data: NDArray, ch_names: List[str]) -> mne.io.RawArray:
        """
        Convert the ndarray board data to mne object
        :param board_data: raw ndarray from board
        :return:
        """
        board_data[:-1, :] = board_data[:-1, :] / 1000000  # BrainFlow returns uV, convert to V for MNE

        # Creating MNE objects from BrainFlow data arrays
        ch_types = ['eeg'] * len(ch_names) + ['stim']
        info = mne.create_info(ch_names=ch_names + ['STIM'], sfreq=self.sfreq, ch_types=ch_types)

        montage = mne.channels.make_standard_montage('biosemi64')
        info.set_montage(montage)
        raw = mne.io.RawArray(board_data, info, verbose=False)
        return raw

    def __get_board_data(self) -> NDArray:
        """The method returns the data from board and remove it"""

        return self.board.get_board_data()

    def __get_raw_data(self, ch_names: List[str]) -> mne.io.RawArray:
        """
        The method returns dataframe with all the raw data, and empties the buffer
        :param ch_names: list[str] of channels to select
        :return: mne_raw data
        """
        ch_names = [ch_name for ch_name in ch_names if not ch_name.startswith(self.empty_channel_prefix)]
        indices = [self.ch_names.index(ch) for ch in ch_names] + \
                  [self.board.get_marker_channel(self.board_id)]
        data = self.data[indices]
        return self.__board_to_mne(data, ch_names)
