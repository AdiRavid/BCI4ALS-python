from datetime import datetime
from typing import Dict



class Config:
    """
    class containing config information for a session.
    This should include any configurable parameters of all the other classes, such as
    directory names for saved data and figures, numbers of trials, train-test-split ratio, etc.
    """

    def __init__(self, name='Synth', num_trials=1):
        # General:
        self.SUBJECT_NAME = name
        self.DATE = datetime.now().strftime('%Y-%m-%d-%H-%M')

        # Headset:
        self.EMPTY_CHANNEL_PREF = 'X'
        self.NUM_EMPTY_CHANNELS = 3
        self.CHANNELS = ['C3', 'C4', 'CZ',
                         'FC1', 'FC2', 'FC5', 'FC6',
                         'CP1', 'CP2', 'CP5', 'CP6',
                         'O1', 'O2']
        self.CHANNELS += [f'{self.EMPTY_CHANNEL_PREF}{i}' for i in range(1, self.NUM_EMPTY_CHANNELS + 1)]

        # Paradigm:
        self.CLASSES = ['LEFT', 'RIGHT']
        self.IDLE_LABEL = 'IDLE'
        self.CLASSES = self.CLASSES[:len(self.CLASSES) // 2] + [self.IDLE_LABEL] + self.CLASSES[len(self.CLASSES) // 2:]
        self.CLASSES_MAP = {label: i for i, label in enumerate(self.CLASSES, start=1)}

        self.NUM_TRIALS_PER_CLASS = num_trials
        self.TIME_PER_TRIAL = 1
        self.TIME_BETWEEN_TRIALS = 1

        # UI:
        self.CLASSES_IMS = {val: f'ui/resources/{val.lower()}.png' for val in self.CLASSES}

        # This needs to be an dict where the keys are stim values and the values are their labels
        # TRIAL_LABELS: Dict[int, str] = dict()
        self.TRIAL_LABELS = {"LEFT": 1, "RIGHT": 2, "NONE": 3}
        # Set trial start and end times in seconds relative to stimulus (for example -0.2, 0.9)
        self.TRIAL_START_TIME = -0.1
        self.TRIAL_END_TIME = 0.5

        # PREPROCESSING:
        self.SESSION_SAVE_DIR = '../..'
        self.HIGH_PASS_FILTER = 0.1
        self.LOW_PASS_FILTER = 40
        self.NOTCH_FILTER = 50

        # CLASSIFICATION:
        self.NUM_OF_FEATURES = 10