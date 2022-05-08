import brainflow
import numpy as np
import pyqtgraph as pg
from brainflow.board_shim import BoardShim, BrainFlowError
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations
from pyqtgraph import ViewBox, intColor
from pyqtgraph.Qt import QtGui, QtCore


class Graph:
    def __init__(self, board_shim, ch_names, config):
        self.board_id = board_shim.get_board_id()
        self.board_shim = board_shim
        self.exg_channels = BoardShim.get_exg_channels(self.board_id)
        self.sampling_rate = BoardShim.get_sampling_rate(self.board_id)
        self.update_speed_ms = 50
        self.window_size = 5
        self.num_points = self.window_size * self.sampling_rate
        self.ch_names = ch_names
        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsWindow(title='BrainFlow Plot',size=(800, 600))
        self.config = config
        self._init_timeseries()

        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(self.update_speed_ms)
        QtGui.QApplication.instance().exec_()


    def _init_timeseries(self):
        self.plots = list()
        self.curves = list()
        self.psd_curves = list()
        self.psd = self.win.addPlot(row=0, col=1, rowspan=len(self.exg_channels))
        self.psd.setTitle('Power Spectrum')
        self.psd.enableAutoRange(ViewBox.YAxis)
        self.psd.addLegend((-20, 10))
        for i in self.config.REAL_CHANNEL_INDXS:
            p = self.win.addPlot(row=i,col=0)
            p.showAxis('left', True)
            p.setLabel('left', self.ch_names[i], 'uV')
            p.setMenuEnabled('left', False)
            p.showAxis('bottom', False)
            p.setMenuEnabled('bottom', False)
            p.disableAutoRange(ViewBox.YAxis)
            p.setRange(yRange=(-50, 50))
            if i == 0:
                p.setTitle('TimeSeries Plot')
            self.plots.append(p)
            color = intColor(i, hues=len(self.exg_channels))
            curve = p.plot(pen=color, name=self.ch_names[i])
            self.curves.append(curve)
            curve = self.psd.plot(connect='all', pen=color, name=self.ch_names[i])
            self.psd_curves.append(curve)




    def update(self):
        data = self.board_shim.get_current_board_data(self.num_points)
        data *= (24 // self.config.GAIN_VALUE)
        for count, channel in enumerate(self.exg_channels[:len(list(self.config.REAL_CHANNEL_INDXS))]):
            # plot timeseries

            DataFilter.detrend(data[channel], DetrendOperations.CONSTANT.value)
            DataFilter.perform_highpass(data[channel], self.sampling_rate, 1, 2,
                                        FilterTypes.BUTTERWORTH.value, 0)
            DataFilter.perform_lowpass(data[channel], self.sampling_rate, 50, 2,
                                       FilterTypes.BUTTERWORTH.value, 0)
            # DataFilter.perform_bandpass(data[channel], self.sampling_rate, 51.0, 100.0, 2,
            #                             FilterTypes.BUTTERWORTH.value, 0)
            # DataFilter.perform_bandpass(data[channel], self.sampling_rate, 51.0, 100.0, 2,
            #                             FilterTypes.BUTTERWORTH.value, 0)
            DataFilter.perform_bandstop(data[channel], self.sampling_rate, 50.0, 4.0, 2,
                                        FilterTypes.BUTTERWORTH.value, 0)
            # DataFilter.perform_bandstop(data[channel], self.sampling_rate, 60.0, 4.0, 2,
            #                             FilterTypes.BUTTERWORTH.value, 0)
            self.curves[count].setData(data[channel].tolist())
            try:
                amp, freq = DataFilter.get_psd(data[channel, -512:], self.sampling_rate, brainflow.WindowFunctions.HAMMING.value)
            except BrainFlowError:
                # When the data starts arriving there arent 512 points to do fft so get_psd will raise an error.
                freq = np.arange(0, 125)
                amp = np.zeros_like(freq)
            self.psd_curves[count].setData(freq.tolist(), amp.tolist())
        self.app.processEvents()