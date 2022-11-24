# Data preparation for IMDA Audio

This python script cleans and prepares the data sourced from IMDA National Speech Corpus, which contains more than 1TB worth of recordings. Due to logistical setup issues, only a subset of data can be used for training.

### Table of Contents

- [About](#About)
- [Motivation](#Motivation)
- [Data description](#Data-description)
- [Usage](#Usage)
- [Credits](#Credts)
- [TODO](#TODO)
- [Contributing](#Contributing)

File structure as per DeepSpeech requirements:
```
ds_dataset
|
|__clips
|   |
|   |_ audiofile1.wav 
|   |_ audiofile2.wav
|   |_ ..
|__wav_files
|   |
|   |_audiofile1_chunk1.wav 
|   |_audiofile1_chunk2.wav
|   |_...
|   |_train.csv
|   |_dev.csv
|   |_test.csv
|
|__textgrid_files
|   |
|   |_audiofile1.TextGrid
|   |_audiofile2.TextGrid
|   |_...
|   |_transcript.csv
|__alphabet.txt               
|__checkpoint


```

## About
The National Speech Corpus (NSC) is the first large-scale Singapore English corpus spearheaded by the Info-communications and Media Development Authority of Singapore (IMDA). Their primary aim to to become an important source of open speech data for automatic speech recognition (ASR) research and speech-related applications (source: https://www.isca-speech.org/archive_v0/Interspeech_2019/pdfs/1525.pdf). It contains more than 1TB worth of recordings with Singaporean accents. Part of the recordings were used to fine-tune the pre-existing DeepSpeech acoustic model to better perform on Singaporean accents. Due to logistical issues, I used 43.1GB of IMDA's data for fine-tuning.

## Motivation
The pre-existing acoustic model provided by DeepSpeech seems to perform poorly on asian origins upon testing on Singaporean videos on YouTube. Since the users of our application would mostly be Singaporeans, addtional fine-tuning to Singaporean accents would be ideal. 

Read more on [AutoSub](https://github.com/qlchan24/AutoSub)

## Data description
DeepSpeech requires the dataset to be passed to be of a [certain format](https://github.com/mozilla/deepspeech-playbook/blob/master/DATA_FORMATTING.md). The raw dataset from IMDA consists of an average of 20min audio files, together with the TextGrid files containing their corresponding transcripts. Each speaker's metadata was also documented. I used the Debate and Finance + Emotion audio and scripts from PART 5.

## Usage
After passing through the desired path for audio storage, the script first attempts to split the supplied audio files into chunks from the specifed timestamp provided in the TextGrid files. After which it splits the dataset into train, dev, test for preparation of training. Silent audio, empty transcripts, very short audio files and unknown characters are filtered away in the final csv files to improve accuracy. A Docker environment was used for training as per documented in the [DeepSpeech Playbook](https://mozilla.github.io/deepspeech-playbook/). 

```python 

    # pass in your own path to the audio files and see the magic happen!
    convert_textgrid_to_csv("/home/tzeminhhhh/ds_dataset", "/home/tzeminhhhh/ds_dataset/clips") 

```

3 csv files -- `train.csv, dev.csv, test.csv` are generated with columns: wav_filename, wav_filesize, transcript, as per required in the documention. An additional transcript.csv is also generated in the `textgrid_files` directory. It contains all the filenames, filesize and transcript from train, dev and test for easy reference.


## Credits
Snippets of code were used in the formulation of this script. Credits to: [PyDub](https://github.com/jiaaro/pydub), [natsort](https://pypi.org/project/natsort/), and of course the trusty StackOverflow and Google!

## TODO
Some of the audio files provided by IMDA is not in the desired sample rate of 16kHz as required. Additional work needs to be done to convert the sample rate of these files.
## Contributing 
Pull requests are welcome. Do open an issue to raise any changes! :smile:
