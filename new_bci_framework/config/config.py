import datetime


class Config:
    """
    class containing config information for a session.
    This should include any configurable parameters of all the other classes, such as
    directory names for saved data and figures, numbers of trials, train-test-split ratio, etc.
    """

    SUBJECT_NAME = ""
    DATE = datetime.datetime.now().date().isoformat()
    NUM_TRIALS = 10
    CLASSES = {1: "LEFT", 2: "RIGHT", 3: "NONE"}

