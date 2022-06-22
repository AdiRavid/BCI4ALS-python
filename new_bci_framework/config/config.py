from datetime import datetime
from typing import Dict



class Config:
    """
    class containing config information for a session.
    This should include any configurable parameters of all the other classes, such as
    directory names for saved data and figures, numbers of trials, train-test-split ratio, etc.
    """

    def __init__(self, num_trials=1, synth=False):
        # GENERAL:
        self.SUBJECT_NAME = 'Synth' if synth else 'Subject'
        self.DATE = datetime.now().strftime('%Y-%m-%d-%H-%M')

        # HEADSET:
        self.GAIN_VALUE = 4
        HARDWARE_GAIN_SETTINGS = {6: "x1030110Xx2030110Xx3030110Xx4030110Xx5030110Xx6030110Xx7030110Xx8030110XxQ030110"
                                     "XxW030110XxE030110XxR030110XxT030110XxY131000XxU131000XxI131000X ",
                                  4: "x1020110Xx2020110Xx3020110Xx4020110Xx5020110Xx6020110Xx7020110Xx8020110XxQ020110"
                                     "XxW020110XxE020110XxR020110XxT020110XxY121000XxU121000XxI121000X "}
        self.HARDWARE_GAIN_MSG = HARDWARE_GAIN_SETTINGS.get(self.GAIN_VALUE, None)

        self.CHANNELS = ['C3', 'C4', 'Cz',
                         'FC1', 'FC2', 'FC5', 'FC6',
                         'CP1', 'CP2', 'CP5', 'CP6']
        self.REAL_CHANNEL_INDICES = range(len(self.CHANNELS))
        self.EMPTY_CHANNEL_PREF = 'X'
        self.NUM_EMPTY_CHANNELS = 16 - len(self.CHANNELS)
        self.CHANNELS += [f'{self.EMPTY_CHANNEL_PREF}{i}' for i in range(1, self.NUM_EMPTY_CHANNELS + 1)]
        self.MONTAGE_FILENAME = r"new_bci_framework/recorder/montage.loc"

        # PARADIGM:
        self.CLASSES = ['LEFT', 'IDLE', 'RIGHT']
        self.LABELS2MARKERS: Dict[str, int] = {label: i for i, label in enumerate(self.CLASSES, start=1)}
        self.MARKERS2LABELS: Dict[int, str] = {i: label for i, label in enumerate(self.CLASSES, start=1)}
        self.NUM_TRIALS_PER_CLASS = num_trials

        # UI:
        self.PRE_CUE_LENGTH = 2
        self.PAUSE_LENGTH = 1
        self.CUE_LENGTH = 2

        self.CLASSES_IMS = {val: f'new_bci_framework/ui/recording_ui/resources/{val.lower()}.png' for val in self.CLASSES}

        # PREPROCESSING:
        self.SESSION_SAVE_DIR = '../..'
        self.HIGH_PASS_FILTER = 1
        self.LOW_PASS_FILTER = 45
        self.NOTCH_FILTER = 50

        # SEGMENTATION
        # Set trial start and end times in seconds relative to stimulus (for example -0.2, 0.9)
        self.TRIAL_START_TIME = -0.5  # -0.1
        self.TRIAL_END_TIME = 2.5  # 0.5

        # CLASSIFICATION:
        self.NUM_OF_FEATURES = 20
        self.NEW_MODEL = True  # TODO: if you wand to create a new model - set to TRUE (else- will update the existing model)
        self.MODEL_PATH = f'model.sav'
