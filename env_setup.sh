#!/bin/sh

# caution this script is untested.

# assumes pipenv managed virtual env is activated
pipenv install SpeechRecognition

# install port audio
brew install portaudio
pipenv install pyaudio

# install FFmpeg for youtube music
brew install ffmpeg
