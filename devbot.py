import subprocess
import speech_recognition as sr  # import the library
import logging
import play

WAKE_WORD = "Alfred"
# supported commands
TERMINATE_CMDS = ["thatll be all", "that will be all"]  # ' are removed
HELP_CMD = "list commands"
PLUGIN_CMDS = {}
VOICE_ALIAS_CMDS = {}
# static variables
APP_NAME = "devbot"
CSV_DELIM = ","
VOICE_ALIAS_FILE = "cmd_alias_map.csv"
# logger
LOG = logging.getLogger(APP_NAME)
LOG.setLevel(logging.WARN)
FORMAT = '%(asctime)s - %(name)s - %(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT)


def receive_cmd_and_run():
    r = sr.Recognizer()  # initialize recognizer
    with sr.Microphone() as source:  # mention source it will be either Microphone or audio files.
        LOG.debug("listening for audio input...")
        audio = r.listen(source)  # listen to the source
        try:
            text = r.recognize_google(audio)  # use recognizer to convert our audio into text part.

            if WAKE_WORD in text:
                cmd = text.replace(WAKE_WORD, "")
                cmd = cmd.replace("'", "")
                cmd = cmd.strip()
                print("Thank you. I heard: " + cmd)
                if cmd in TERMINATE_CMDS:
                    print("Stopping. Goodbye")
                    return False
                elif cmd == HELP_CMD:
                    print(cmd_list())
                else:
                    process_command(cmd)
            else:
                LOG.debug("no wake word found (" + WAKE_WORD + ")")

        except ValueError:
            print("Sorry could not recognize your voice")  # In case of voice not recognized  clearly
        except sr.UnknownValueError:
            LOG.debug("received unknown value error")
        except subprocess.CalledProcessError:
            print("Sorry command: '" + cmd + "' is not supported, please try another")
    return True


def cmd_list():
    tab = "   "
    cmds = ""
    for cmd in TERMINATE_CMDS:
        cmds += tab + cmd + "\n"
    for cmd in PLUGIN_CMDS:
        cmds += tab + cmd + "\n"
    for cmd in VOICE_ALIAS_CMDS:
        cmds += tab + cmd + "\n"
    return cmds


def process_command(command):
    LOG.debug("running command: " + str(command))
    command = command.lower()
    if process_plugin(command):
        return
    else:
        alias = get_alias(command)
        full_cmd = "/bin/bash -i -c " + alias
        subprocess.check_output(full_cmd, stderr=subprocess.STDOUT, shell=True)


def process_plugin(command):
    for name in PLUGIN_CMDS:
        plugin = PLUGIN_CMDS[name]
        if plugin.supports_command(command):
            plugin.run_action(command)
            LOG.debug("ran plugin: " + plugin.get_name())
            return True
    return False


def get_alias(command):
    if command in VOICE_ALIAS_CMDS:
        return VOICE_ALIAS_CMDS[command]
    else:
        LOG.debug("no voice alias found trying to run " + command)
        return command


def run_command(text):
    command = text
    # convert command to bash script name
    command = command.strip()
    command = command.replace(" ", "_")
    command = "actions/" + command + ".sh"
    cmd_list = ["/bin/bash", command]

    # run command
    LOG.debug("running command: " + str(cmd_list))
    list_files = subprocess.run(cmd_list)
    LOG.debug("The exit code was: %d" % list_files.returncode)


def populate_plugins():
    PLUGIN_CMDS['play'] = play.YoutubePlayList()


def populate_bash_alias():
    with open(VOICE_ALIAS_FILE) as f:
        content = f.readlines()
        for line in content:
            line = line.strip()
            if line != "":
                key, value = line.split(CSV_DELIM)
                key = key.strip()
                value = value.strip()
                VOICE_ALIAS_CMDS[key] = value
                logging.debug("added to voice alias: " + key + "=" + value)


def start():
    print("hello, I'm devbot " + WAKE_WORD + "! What can I help you with?")
    while receive_cmd_and_run():
        pass


def main():
    LOG.info("starting " + APP_NAME)
    populate_plugins()
    populate_bash_alias()
    start()


if __name__ == "__main__":
    main()
