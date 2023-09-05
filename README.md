# Dataset
### About Dataset
## Description

We collected EEG signal data from 10 college students while they watched MOOC video clips. We extracted online education videos that are assumed not to be confusing for college students, such as videos of the introduction of basic algebra or geometry. We also prepare videos that are expected to confuse a typical college student if a student is not familiar with the video topics like Quantum Mechanics, and Stem Cell Research. We prepared 20 videos, 10 in each category. Each video was about 2 minutes long. We chopped the two-minute clip in the middle of a topic to make the videos more confusing.
The students wore a single-channel wireless MindSet that measured activity over the frontal lobe. The MindSet measures the voltage between an electrode resting on the forehead and two electrodes (one ground and one reference) each in contact with an ear.
After each session, the student rated his/her confusion level on a scale of 1-7, where one corresponded to the least confusing and seven corresponded to the most confusing. These labels if further normalized into labels of whether the students are confused or not. This label is offered as self-labelled confusion in addition to our predefined label of confusion.

Dataset link: https://www.kaggle.com/datasets/wanghaohan/confused-eeg
## Content
These data are collected from ten students, each watching ten videos. Therefore, it can be seen as only 100 data points for these 12000+ rows. If you look at this way, then each data point consists of 120+ rows, which is sampled every 0.5 seconds (so each data point is a one minute video). Signals with higher frequency are reported as the mean value during each 0.5 second.

EEG_data.csv: Contains the EEG data recorded from 10 students

demographic.csv: Contains demographic information for each student

video data : Each video lasts roughly two-minute long, we remove the first 30 seconds and last 30 seconds, only collect the EEG data during the middle 1 minute.

## Acknowledgements
Wang, H., Li, Y., Hu, X., Yang, Y., Meng, Z., & Chang, K. M. (2013, June). Using EEG to Improve Massive Open Online Courses Feedback Interaction.


# Template transformation block (Python)
Transformation blocks take raw data from your [organizational datasets](https://docs.edgeimpulse.com/docs/tutorial-building-your-first-dataset) and convert the data into files that can be loaded in an Edge Impulse project. You can use transformation blocks to only include certain parts of individual data files, calculate long-running features like a running mean or derivatives, or efficiently generate features with different window lengths. Transformation blocks can be written in any language, and run on the Edge Impulse infrastructure.

Learn more about creating a custom transformation block: https://docs.edgeimpulse.com/docs/creating-a-transformation-block-dataset

# Justfile

This repository contains a Justfile with several commands to facilitate building, running, and pushing Docker images and interacting with Edge Impulse.

## Commands

### build
This command builds a Docker image and tags it with the name of the current directory.


just build

### run-shell
This command starts a shell within the Docker container to facilitate local debugging.

just run-shell

### run-with-mount-and-entrypoint
This command runs a Docker container with a local directory mounted to a directory in the container and a custom entrypoint. Replace local_dir with the path of the local directory you want to mount and container_dir with the corresponding directory in the container.

just run-with-mount-and-entrypoint "/path/to/local_dir" "/path/to/container_dir"

### push
This command pushes the block to Edge Impulse.

just push

### Usage
To use the commands defined in this Justfile, make sure you have Just installed on your system.

Once Just is installed, you can run the commands by executing just followed by the command name in the terminal.

For example, to build the Docker image, use the following command:

just build

Make sure you are in the root directory of the repository when running the commands.
