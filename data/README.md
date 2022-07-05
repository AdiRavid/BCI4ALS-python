# _Data_ 
#### This README's purpose is to describe the raw data files.

## General
___
Over 900 trial were recorded from the mentor and over 700 from us - all the recordings can be found [here](https://drive.google.com/drive/u/0/folders/1rp6hpcxEi11E6CE1mR3opdyKGXiShJSd). 

Unfortunately, most of the data from the mentor was very noisy, as will be described in this README.

## Mentor Python Recordings
___
Most recordings from the mentor were obtained using the python CytonRecorder class and are saved in the format **Subject_yyyy-mm-dd-hh-mm_raw.fif**.

Out of over 900 recording, after rejecting bad epochs during preprocessing, only around 100 were not dropped.
In addition, most remaining trails were either 'LEFT' or 'RIGHT':  
![img.png](README_resources/epochs_dist.png)

### 28-04-2022:
* 270 trials in 4 different recordings.
* Due to an indices problem, the raw files channel names were saved with an offset such that the first channel which should be C3 is actually irrelevant and C3 was saved in the second channel. C4 is in the third and so on, so that CP6 is missing in all of these files.  
![img.png](README_resources/indices_problem.png)

### 08-05-2022:
* 240 trials in 3 different recordings.
* Here all channels are present but a lot of the recording is very noisy:  
![img_1.png](README_resources/subject_raw.png)

### 15-05-2022:
* 369 trials in 5 different recordings.
* Data is very noisy as well.

## Matlab Recordings
A small portion of recordings from the mentor were obtained using the python CytonRecorder class and are saved in the format **Subject_yyyy-mm-dd-hh-mm_raw.fif**.
___
* Saved in the directory 'xdf_files'
* 54 trials in 3 different recording.
* The amplitude values in the matlab recordings differ greatly than those in the python recordings. We tried combining them by normalizing the data, but eventually decided to treat each data set differently.
* The signal here is also not good (either very flat or very noisy):  
![img_3.png](README_resources/subject_raw_matlab.png)

## Sivan's Python Recordings
___
* In the directory named Sivan there are recording files which are not from the mentor, but from Sivan, a team member.
* 720 events in 12 different recordings.
* Very good data:  
![img_2.png](README_resources/sivan_raw.png)

## Recordings from 07-05-2022:
To eliminate the mentor's house as the cause of noise (due to a lot of electrical machines), we recorded 2 recordings at the same location, on the same day, under similar settings, once on Sivan and once on the mentor.
The results rule out the location as the cause for noise, but raise many new questions.
We hypothesize that some of the noise may come from the respirator.
![img.png](README_resources/Sivan_mentor_comp.png)