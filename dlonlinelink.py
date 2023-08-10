#import helpers.csvhelper as csvhelper
#import helpers.filehelper as filehelper
import helpers.urlhelper as urlhelper

#import vlc
#import pafy
from sys import platform as PLATFORM
import yt_dlp
from yt_dlp import YoutubeDL
# eyeD3 import eyeD3
from configparser import ConfigParser
from tinytag import TinyTag
#import urllib
#from urllib.error import HTTPError
#import validators
#from validators import ValidationFailure
#import requests

#Load Config
config = ConfigParser()
config.read('config.ini')

#global videoFilePath
#videoFilePath = config['main_section'].get('videofolder_path')

global finalFilename



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
        
# ℹ️ See "progress_hooks" in help(yt_dlp.YoutubeDL)
def my_hook(d):
    if d['status'] == 'finished':
        #test.lol_return_value(d['filename'])
        global finalFilename
        finalFilename =  d['filename']
        print('finalFilename ' + finalFilename)

    if d['status'] == 'downloading':
        #test.lol_return_value(d['filename'])
        
        print('Downloading see if you can log here')
        #global finalFilename
        #finalFilename =  d['filename']
        #print('finalFilename ' + finalFilename)

    if d['status'] == 'error':
        #test.failed_return()
        print("Could not find video for link")
    






def try_get_link(URLIn, videofolder_path):


    ydl_opts = {
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
        'outtmpl' : videofolder_path + '\\~TEMP\\%(title)s.%(ext)s'
    }

    from yt_dlp import YoutubeDL
    if(urlhelper.is_path_url(URLIn) and urlhelper.url_ok(URLIn)):
        #URLS = [song["ONLINE_PATH"]]
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(URLIn)
    else:
        print("Cannot find video for " + URLIn + " skipping...")
        return None
        #new_songDict.append(song)
    return finalFilename

