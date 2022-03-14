import datetime


class Config:
    """
    class containing config information for a session.
    This should include any configurable parameters of all the other classes, such as
    directory names for saved data and figures, numbers of trials, train-test-split ratio, etc.
    """

    SUBJECT_NAME = ""
    DATE = datetime.datetime.now().date().isoformat()
    CHANNELS = ['C3', 'C4', 'CZ',
                'FC1', 'FC2', 'FC5', 'FC6',
                'CP1', 'CP2', 'CP5', 'CP6',
                'O1', 'O2', 'X1', 'X2', 'X2']
    NUM_TRIALS = 3
    CLASSES = {1: "LEFT", 2: "RIGHT", 3: "NONE"}

