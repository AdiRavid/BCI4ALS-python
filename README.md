# _bci4als-2022-python_ 
___

#### Python framework for the 2022 BCI4ALS course by team 33 HUJI.

_Some of the code in the beginning was taken from team 34 HUJI._

## Basic Usage
___

In almost every directory there is a file that specifies the desired behaviour for this type of class.

In order to run our framework run main.py. 

* main.py - **TODO - add description of main once we know what we want to have there.** 

## classifier
___
**TODO - add our classifiers, maybe add all?**

* base_classifier.py - the basic API that all classifiers need to follow.
* optuna_runner.py - contains the function "run_optuna" which runs optuna (A hyperparameter optimization framework) for 
xgb classifier.
  
 
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

**TODO - understand if we need it and if so what, I don't think we need the plot_raw_data**

* plot_epochs.py - we use this code to plot the average of epochs by class for a single fif file.

## preprocessing
___

**TODO - delete the file preprocessing.py we use the other one.**

* preprocessing_pipeline.py - this class contains the preprocessing we perform on the raw data; filtering, segmentation, auto-reject,
and feature extraction.

## recorder 
___

**TODO - delete the files: plot_rt_recording_old.py, test.py, montage.loc (we use the predefined montage) and complete 
the missing description**

* open_bci_cyton_recorder.py - 
* plot_rt_recording.py - allows us to see the recording in real time in python before starting the recording.
* recorder.py - 

## session
___

* session.py - the basic API that all sessions should follow.
* offline_session.py - this class is responsible for running an offline training session.
* co_adaptive_session.py - this class is responsible for running an online training session (with feedback).

## ui
___

* ui.py - the basic API that all ui should follow.
* offline_ui.py - this class is responsible for the ui of an offline session.
* co_adaptive_ui.py - this class is responsible for the ui of an online session (with feedback).
* resources: (images for offline ui)
  * idle.png
  * left.png
  * right.png
* car dodge game PYTHON - (**TODO: maybe change the name?**)
  * **TODO - choose the relevant files**

  