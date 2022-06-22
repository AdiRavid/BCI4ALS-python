# _bci4als-2022-python_ 
___

#### Python framework for the 2022 BCI4ALS course by team 33 HUJI.

_General framework and part of the code in the recorder classes was taken from HUJI team 34 (2021-2022) - 
https://github.com/AviH0/bci4als-2022-python/tree/main/new_bci_framework._

## Basic Usage
___

In almost every directory there is a file that specifies the desired behaviour for this type of class.

In order to run our framework run main.py. 

* main.py - **TODO - add description of main once we know what we want to have there.** 

## classifier
___

* base_classifier.py - the basic API that all classifiers need to follow.
* dummy_classifier.py - Dummy classifier that returns random prediction.
* ensemble_classifier.py - Ensemble classifier of xgb models. the ensemble is an array of xgb model, that decide using the "major vote".  
* xgb_classifier.py - XGB classifier.
* random_forest_classifier.py - Random Forest classifier.
* logistic_regression_classifier.py - Logistic Regression classifier.  
* optuna_runner.py - contains 3 functions which runs optuna (A hyperparameter optimization framework) for 
xgb classifier, RandomForest classifier and LogisiticRegression classifier.
  
  
 
## config
___

* config.py  - this file contains the config class of a session; This should include any configurable parameters of all
  the other classes, such as directory names for saved data, numbers of trials, electrodes location, etc.


## paradigm
___

* paradigm.py - the basic API that all paradigms should follow.
* MI_paradigm.py - contains the class MIParadigm, which is a sub-class of paradigm for Motor Imagery with 3 classes
  (Left, Right, Idle).


## plotting
___

* plot_epochs.py - we use this code to plot the average of epochs by class for a single fif file. 
  The script also plots average psd for each class as well as average eeg epoch.  

## preprocessing
___

* preprocessing_pipeline.py - this class contains the preprocessing we perform on the raw data:
    filtering(highpass/lowpass + notch), segmentation, auto-reject (with ica), baseline correction, laplacian and feature extraction.

## recorder 
___
Takes care of all aspects of recording the eeg data.
* **recorder.py** - Defines the class `Recorder` - public API for starting and stopping a recording, for pushing markers if a recording is in progress and for retrieving the data from the last recording as mne.Raw.
* **cyton_recorder.py** - Implements the class `CytonRecorder`, a subclass of `Recorder` which implements recording via a Cyton board.
* **plot_rt_recording.py** - Implementation for real time plotting of the eeg signal from the recorder.
* **montage.loc** - A file specifying the location of the used electrodes on the helmet (i.e. on the subject's head).  

## session
___
The 'manager' of a recording session: runs the recording, the preprocessing and the classification.
* **session.py** - Defines the class `Session` - a base class and a public API for an EEG session. This class also implements some shared features of all sessions.
* **offline_session.py** - this class is responsible for running an offline training session.
* **feedback_session.py** - this class is responsible for running an online training session (with feedback).

## recording ui
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


  