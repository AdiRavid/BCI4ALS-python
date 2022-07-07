# _BCI4ALS 2022 - HUJI Team 33_ 
___
#### Generating a BCI tool which one day will allow our mentor to move his wheelchair despite his ALS
Contact us:
* [Maysan Bader](mailto:maysan.bader@mail.huji.ac.il)
* [Sivan Levin](mailto:sivan.levin@mail.huji.ac.il)
* [Shay Grunwald](mailto:shay.grunwald@mail.huji.ac.il)
* [Adi Ravid](mailto:adi.ravid1@mail.huji.ac.il)


#### _Also look at the [data README](README-Data.md)_

## new_bci_framework
___
#### Python framework for the 2022 BCI4ALS course by team 33 HUJI.

_General framework and part of the code in the recorder classes was taken from 
[HUJI team 34 (2021-2022)](https://github.com/AviH0/bci4als-2022-python/tree/main/new_bci_framework._)._ 


### Basic Usage
___
In almost every directory there is a file that specifies the desired behaviour for this type of class.

In order to run our framework run main.py.

* main.py - creates a session (currently offline setting) which holds all the components of a session, and can run any step separately or the entire pipeline. 

### config
___
* **config.py**  - this file contains the config class of a session; This should include any configurable parameters of all
  the other classes, such as directory names for saved data, numbers of trials, electrodes location, etc.

### session
___
The 'manager' of a recording session: runs the recording, the preprocessing and the classification.
* **session.py** - Defines the class `Session` - a base class and a public API for an EEG session. This class also implements some shared features of all sessions.
* **offline_session.py** - Implements the class `OfflineSession`, a subclass of `Session` - responsible for running an offline training session.
* **feedback_session.py** - Implements the class `FeedbackSession`, a subclass of `Session` - responsible for running an offline training session using a feedback loop.

### paradigm
___
* **paradigm.py** - Defines the class `Paradigm` - public API for the experiment's paradigms.
* **MI_paradigm.py** - Implements the class `MIParadigm`, a subclass of `Paradigm` - used for generating Motor Imagery events (according to configuration file).
* **p300_paradigm.py** - Defines the class `P300Paradigm`, a subclass of `Paradigm` - used for generating P300 events. Currently, not implemented.


### recorder 
___
Takes care of all aspects of recording the eeg data.
* **recorder.py** - Defines the class `Recorder` - public API for starting and stopping a recording, for pushing markers if a recording is in progress and for retrieving the data from the last recording as mne.Raw.
* **cyton_recorder.py** - Implements the class `CytonRecorder`, a subclass of `Recorder` which implements recording via a Cyton board.
* **plot_rt_recording.py** - Implementation for real time plotting of the eeg signal from the recorder.
* **montage.loc** - A file specifying the location of the used electrodes on the helmet (i.e. on the subject's head).  

### ui/recording_ui
___
 These classes are in charge of the experiment's recording phase GUI. 
 They implement a user-interface for running the paradigm and collecting data from the subject.
* **recording_ui.py** - Defines the class `RecordingUI`, a public API for recording phase GUIs. This class also implements some shared features of all UIs.
* **offline_recording_ui.py** - Implements the class `OfflineRecordingUI`, a subclass of `RecordingUI` - responsible for the UI of an offline session.
* **feedback_recording_ui.py** - Implements the class `FeedbackRecordingUI`, a subclass of `RecordingUI` - responsible for the UI of a session with a feedback-loop.
* **resources**: (images for UIs)
  * idle.png
  * left.png
  * right.png
  * soccer_ball.png
  * soccer_field.png
  * soccer_player.png

### preprocessing
___
* **preprocessing_pipeline.py** - Defines the class `PreprocessingPipeline` containing all preprocessing steps performed on the raw data:
  * filtering(highpass/lowpass + notch)
  * segmentation 
  * auto-reject (with ica)
  * baseline correction
  * laplacian
  * feature extraction

### classifier
___
* **base_classifier.py** -  Defines the class `BaseClassifier` - public API for classification (mimicking the sklearn API). Also implements feature selection for all subclasses of classifiers. 
* **dummy_classifier.py** - A dummy classifier returning random prediction.
* **xgb_classifier.py** - XGB classifier.
* **random_forest_classifier.py** - Random Forest classifier.
* **logistic_regression_classifier.py** - Logistic Regression classifier.  
* **ensemble_classifier.py** - Ensemble classifier of xgb models. The ensemble is an array of xgb models that decide using "major voting".  
* **optuna_runner.py** - A helper file containing 3 functions which runs optuna (A hyperparameter optimization framework) for xgb classifier, RandomForest classifier and LogisiticRegression classifier.

### plotting
___
Utilities for plotting
* **plot_epochs.py** - we use this code to plot the average of epochs by class for a single fif file. 
  The script also plots average psd for each class as well as average eeg epoch.  

  
## archived_code
___
_Unused code, mostly old classifiers._