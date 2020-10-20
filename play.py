from __future__ import unicode_literals
import sys
import subprocess


class Plugin:
    def run_action(self, data):
        pass

    def supports_command(self, command):
        pass

    def get_name(self):
        return "plugin interface"


class YoutubePlayList(Plugin):
    space = " "

    def __init__(self, play_list_path="actions/youtube_playlists"):
        self.play_list_path = play_list_path

    def _read_playlist(self, file_name):
        file_uri = self.play_list_path + "/" + file_name + ".txt"
        print("[play] file name is: " + file_uri)
        playlist = []
        with open(file_uri, 'r') as file:
            for line in file.read().split('\n'):
                formatted = line.strip()
                if formatted != "":
                    playlist.append(formatted)
        return playlist

    def supports_command(self, command):
        return command.startswith("play")

    def run_action(self, command):
        cmd_list = command.split(self.space)
        playlist_filename = cmd_list[1]  # guarenteed first is 'play'
        playlist = self._read_playlist(playlist_filename)

        ffplay_cmd = ["/bin/bash", self.play_list_path + "/play_video.sh"]

        for video in playlist:
            vid_ffplay_cmd = ffplay_cmd + [video]
            subprocess.run(vid_ffplay_cmd)
        pass

    def get_name(self):
        return "youtube plugin"


def _parse_args(args):
    if len(args) != 2:
        msg = "\nExpecting only one argument, a play list file.\n"
        msg += "Usage: \n\t$ python play.py my_playlist_file.txt\n"
        sys.exit(msg)
    return args[1]


def main(args):
    playlist_filename = _parse_args(args)
    youtube = YoutubePlayList()
    youtube.run_action(playlist_filename)
    print("play program done")


if __name__ == "__main__":
    main(sys.argv)
