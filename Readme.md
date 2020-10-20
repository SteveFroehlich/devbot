# Devbot
A hacked together app that converts audio to bash alias and runs the corresponding 
command. Devbot also has the ability to run bash and python scripts via python 
plugins.


## Features
 1. Continuously listen for wake word. Ignore other sounds
 2. Use the phase "[Wakeword] that'll be all" to stop execution
 3. Based on user created voice command to bash alias [csv file](cmd_alias_map.csv)
 , run commands
 4. Speak "[Wakeword] list commands" to see all the supported commands
 5. Speak "[Wakeword] play classical music" to play the youtube audio
   in the youtube video [here](actions/youtube_playlists/classical.txt)
   the current video is a collection of classical music.
 
Feature #3's [csv file](cmd_alias_map.csv) currently expects two bash alias to be
defined in your .bashrc or .bash_profile to work properly:
```
alias wx='open https://weather.com/weather/today/l/f892433d7660da170347398eb8e3d722d8d362fe7dd15af16ce88324e1b96e70'
alias wxh='open https://weather.com/weather/hourbyhour/l/f892433d7660da170347398eb8e3d722d8d362fe7dd15af16ce88324e1b96e70'
```
Note the default wake word is "Alfred". If can be changed via the 
`WAKE_WORD` varialbe in [devbot.py](devbot.py)


## Usage 
Run `python devbot.py` then speak "Alfred whats the weather" and if you are on a
mac you should see the weather forecast (For New York) open in your default browser.
You can also speak "Alfred list commands" to see all the commands supported out of the
box. The are:
```
(devbot_audio_bot) mac@steve: devbot_audio_bot$ python devbot.py 
hello, I'm devbot Alfred! What can I help you with?
Thank you. I heard: list commands
   thatll be all
   that will be all
   play
   whats the weather
   whats the hourly weather
```
Devbot will print out "Thank you. I heard: some command" to let you know what
its trying to do. The commands are listed below. Not that play is the base command
to play audio from youtube videos. For example "Alfred play classical music" is
the only supported play action currently.

### Installation
You can install via pip: 
```
pip install -r requirements.txt
```
or you can use pipenv. Note port audio needs to be installed as well
if you are on a mac you can use Homebrew:
```
brew install portaudio
```
To run the youtube and music commands you will need FFmpeg. Homebrew
should be able to help there as well
```
brew install ffmpeg
```


###Debugging 
If you are having issues change `LOG.setLevel(logging.WARN)` to
`LOG.setLevel(logging.DEBUG)` in [devbot.py](devbot.py)


### Gotchas
If you play music through speakers instead of headphones the music
can interfere with your voice commands. You try muting the music while you're
giving commands in that case.

 
## Tech
 * [PyAudio](https://pypi.org/project/PyAudio/)
 * [port audio](http://www.portaudio.com/)
 * [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) 
    * [SpeechRecognition github](https://github.com/Uberi/speech_recognition)

To support playing audio from youtube:
 * [youtube-dl](https://pypi.org/project/youtube_dl/)
 * [FFmpeg](https://ffmpeg.org/)
    
   

## Notes on Music with youtube-dl
Resources:
 * [hello world example](https://github.com/ytdl-org/youtube-dl/)
 * [full available options](https://github.com/ytdl-org/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312)


 * add support for watching/listening to youtube
    * `pipenv install youtube-dl`
    * [so post](https://unix.stackexchange.com/questions/160212/watch-youtube-videos-in-terminal)
    * [github](https://github.com/ytdl-org/youtube-dl/)
    * [youtube-dl site](http://ytdl-org.github.io/youtube-dl/about.html)
    * key [SO post](https://stackoverflow.com/questions/50876292/opencv-capture-online-video-for-further-processing-without-downloading-the-file/50881927#50881927)


 ## Resources
 * [toward data science](https://towardsdatascience.com/easy-speech-to-text-with-python-3df0d973b426)
 * [simplified python](https://www.simplifiedpython.net/speech-recognition-python/)
 * [the python code](https://www.thepythoncode.com/article/using-speech-recognition-to-convert-speech-to-text-python)

**Considered but not currently used**
 * [talk back](https://www.geeksforgeeks.org/convert-text-speech-python/)


### Alternatives
[mycroft](https://mycroft.ai/) might be worth looking into.