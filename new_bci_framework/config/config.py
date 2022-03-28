from datetime import datetime
from typing import Dict


class Config:
    """
    class containing config information for a session.
    This should include any configurable parameters of all the other classes, such as
    directory names for saved data and figures, numbers of trials, train-test-split ratio, etc.
    """

    # General:
    SUBJECT_NAME = 'Synth'
    DATE = datetime.now().strftime('%Y-%m-%d-%H:%M')

    # Headset:
    EMPTY_CHANNEL_PREF = 'X'
    NUM_EMPTY_CHANNELS = 3
    CHANNELS = ['C3', 'C4', 'CZ',
                'FC1', 'FC2', 'FC5', 'FC6',
                'CP1', 'CP2', 'CP5', 'CP6',
                'O1', 'O2'] + [f'X{i}' for i in range(1, NUM_EMPTY_CHANNELS + 1)]

    # Paradigm:
    NUM_TRIALS_PER_CLASS = 10
    TIME_PER_TRIAL = 3
    TIME_BETWEEN_TRIALS = 2
    CLASSES = {1: "LEFT", 2: "RIGHT", 3: "NONE"}
    IDLE_LABEL = 'NONE'

    # UI:
    CLASSES_IMS = {1: 'ui/left.png',
                   2: 'ui/right.png',
                   3: 'ui/idle.png'}

    NUM_TRIALS_FOR_PREDICTION = 1
    NUM_TRIALS_FOR_UPDATE = 3

    # This needs to be an dict where the keys are stim values and the values are their labels
    #TRIAL_LABELS: Dict[int, str] = dict()
    TRIAL_LABELS = {"LEFT": 1, "RIGHT": 2, "NONE": 3}
    # Set trial start and end times in seconds relative to stimulus (for example -0.2, 0.9)
    TRIAL_START_TIME = -0.1
    TRIAL_END_TIME = 0.5

    # PREPROCESSING:
    SESSION_SAVE_DIR = '../..'
    HIGH_PASS_FILTER = 0.1
    LOW_PASS_FILTER = 40
    NOTCH_FILTER = 50

    # CLASSIFICATION:
    NUM_OF_FEATURES = 10