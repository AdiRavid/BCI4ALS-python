from datetime import datetime
from typing import Dict



class Config:
    """
    class containing config information for a session.
    This should include any configurable parameters of all the other classes, such as
    directory names for saved data and figures, numbers of trials, train-test-split ratio, etc.
    """

    def __init__(self, num_trials=1, synth=False, selected_feature_path=None):
        # GENERAL:
        self.SUBJECT_NAME = 'Synth' if synth else 'Subject'
        self.DATE = datetime.now().strftime('%Y-%m-%d-%H-%M')

        # HEADSET:
        self.GAIN_VALUE = 4
        self.EMPTY_CHANNEL_PREF = 'X'
        self.CHANNELS = ['C3', 'C4', 'Cz',
                         'FC1', 'FC2', 'FC5', 'FC6',
                         'CP1', 'CP2', 'CP5', 'CP6']
        self.REAL_CHANNEL_INDXS = range(len(self.CHANNELS))
        self.NUM_EMPTY_CHANNELS = 16 - len(self.CHANNELS)
        self.CHANNELS += [f'{self.EMPTY_CHANNEL_PREF}{i}' for i in range(1, self.NUM_EMPTY_CHANNELS + 1)]
        self.MONTAGE_FILENAME = r"new_bci_framework/recorder/montage.loc"


        # PARADIGM:
        self.IDLE_LABEL = 'IDLE'
        self.CLASSES = ['LEFT', f'{self.IDLE_LABEL}', 'RIGHT']
        self.TRIAL_LABELS: Dict[str, int] = {label: i for i, label in enumerate(self.CLASSES, start=1)}

        self.NUM_TRIALS_PER_CLASS = num_trials

        # UI:
        self.PRE_CUE_LENGTH = 2
        self.PAUSE_LENGTH = 1
        self.CUE_LENGTH = 2

        self.CLASSES_IMS = {val: f'new_bci_framework/ui/resources/{val.lower()}.png' for val in self.CLASSES}
        self.PREDICTED_CLASSES_IMS = {val: f'new_bci_framework/ui/resources/{val.lower()}_pred.png' for val in self.CLASSES}


        # PREPROCESSING:
        self.SESSION_SAVE_DIR = '../..'
        self.HIGH_PASS_FILTER = 0.1
        self.LOW_PASS_FILTER = 60
        self.NOTCH_FILTER = 50

        # SEGMENTATION
        # Set trial start and end times in seconds relative to stimulus (for example -0.2, 0.9)
        self.TRIAL_START_TIME = -0.5  # -0.1
        self.TRIAL_END_TIME = 2.5  # 0.5

        # FEATRUE SELECTION:
        self.SELECTED_FEATURES_PATH = selected_feature_path

        # CLASSIFICATION:
        self.NUM_OF_FEATURES = 20
        self.NEW_MODEL = True  # TODO: if you wand to create a new model - set to TRUE (else- will update the existing model)
        self.MODEL_PATH = f'model.sav'
