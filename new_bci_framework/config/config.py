from datetime import datetime
from typing import Dict



class Config:
    """
    class containing config information for a session.
    This should include any configurable parameters of all the other classes, such as
    directory names for saved data and figures, numbers of trials, train-test-split ratio, etc.
    """

    def __init__(self, name='Synth', num_trials=1):
        # GENERAL:
        self.SUBJECT_NAME = name
        self.DATE = datetime.now().strftime('%Y-%m-%d-%H-%M')

        # HEADSET:
        self.EMPTY_CHANNEL_PREF = 'X'
        self.NUM_EMPTY_CHANNELS = 3
        self.CHANNELS = ['C3', 'C4', 'CZ',
                         'FC1', 'FC2', 'FC5', 'FC6',
                         'CP1', 'CP2', 'CP5', 'CP6',
                         'O1', 'O2']
        self.CHANNELS += [f'{self.EMPTY_CHANNEL_PREF}{i}' for i in range(1, self.NUM_EMPTY_CHANNELS + 1)]

        # PARADIGM:
        self.IDLE_LABEL = 'IDLE'
        self.CLASSES = ['LEFT', f'{self.IDLE_LABEL}', 'RIGHT']
        self.TRIAL_LABELS = {label: i for i, label in enumerate(self.CLASSES, start=1)}

        self.NUM_TRIALS_PER_CLASS = num_trials

        # UI:
        self.PRE_CUE_LENGTH = 2
        self.PAUSE_LENGTH = 1
        self.CUE_LENGTH = 3

        self.CLASSES_IMS = {val: f'ui/resources/{val.lower()}.png' for val in self.CLASSES}

        # PREPROCESSING:
        self.SESSION_SAVE_DIR = '../..'
        self.HIGH_PASS_FILTER = 0.1
        self.LOW_PASS_FILTER = 40
        self.NOTCH_FILTER = 50

        # SEGMENTATION
        # Set trial start and end times in seconds relative to stimulus (for example -0.2, 0.9)
        self.TRIAL_START_TIME = -0.1
        self.TRIAL_END_TIME = 0.5

        # CLASSIFICATION:
        self.NUM_OF_FEATURES = 10
        self.MODEL_PATH = f'model.sav'
