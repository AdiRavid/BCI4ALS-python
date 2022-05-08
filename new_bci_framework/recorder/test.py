from time import sleep

from new_bci_framework.recorder.open_bci_cyton_recorder import *
from new_bci_framework.recorder.plot_rt_recording import Graph


def main_test():
    print("creating recorder")
    rec = CytonRecorder(None, board_id=BoardIds.SYNTHETIC_BOARD)
    print("\n------------\ncreated recorder")
    rec.start_recording()
    print("\n------------\nstarted recording")
    th = rec.plot_live_data(block=False)
    sleep(15)
    th.join()
    rec.end_recording()
    print("\n------------\nended recording")
    raw = rec.get_raw_data()

    raw.plot()