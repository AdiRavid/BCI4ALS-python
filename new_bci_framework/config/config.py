from datetime import datetime

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
                'O1', 'O2'] + [f'{EMPTY_CHANNEL_PREF}{i}' for i in range(1, NUM_EMPTY_CHANNELS + 1)]

    # Paradigm:
    NUM_TRIALS_PER_CLASS = 1
    TIME_PER_TRIAL = 1
    TIME_BETWEEN_TRIALS = 1
    CLASSES = {1: "LEFT", 2: "RIGHT", 3: "NONE"}
    IDLE_LABEL = 'NONE'

    # UI:
    CLASSES_IMS = {1: 'ui/left.png',
                   2: 'ui/right.png',
                   3: 'ui/idle.png'}

    NUM_TRIALS_FOR_PREDICTION = 1
    NUM_TRIALS_FOR_UPDATE = 3
