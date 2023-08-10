# eyeD3 import eyeD3
from configparser import ConfigParser

from helpers import urlhelper, csvhelper
from yt_dlp import YoutubeDL


# import vlc
# import pafy
# import urllib
# from urllib.error import HTTPError
# import validators
# from validators import ValidationFailure
# import requests


class MyLogger:
    def debug(self, msg):
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith('[debug] '):
            pass
        else:
            self.info(msg)

    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


# TODO: Try and use custom postprocessor https://pypi.org/project/yt-dlp/
# ℹ️ See "progress_hooks" in help(yt_dlp.YoutubeDL)
def my_hook(d):
    global songList
    global song_index

    song = songList[song_index]

    if d['status'] == 'finished':
        print(d['filename'])
        # print(d["_filename"])
        song['LOCAL_PATH'] = d['filename']
        print(song)
        print('Done downloading, adding to spreadsheet ...')
    if d['status'] == 'error':
        print('Failed to DL song, skipping...')


def main():
    # Load Config
    config = ConfigParser()
    config.read('config.ini')

    ydl_opts = {
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
        'outtmpl': config['main_section'].get('videofolder_path') + '\\~VIDEOTANOSHII\\%(title)s.%(ext)s'
    }

    global videoFilePath
    videoFilePath = config['main_section'].get('videofolder_path')

    global songList
    global song_index

    songList = csvhelper.csvtodict()

    print(songList)
    for i in range(len(songList)):
        song_index = i
        song = songList[i]
        online_path = song["ONLINE_PATH"]
        if (urlhelper.url_ok(online_path)):
            # URLS = [song["ONLINE_PATH"]]
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download(online_path)
        else:
            print("Cannot find video for " + song["ONLINE_PATH"] + " skipping...")
    # Overwrite the CSV
    csvhelper.dicttocsv(songList)


if __name__ == "__main__":
    main()
