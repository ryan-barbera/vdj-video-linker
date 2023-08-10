import dlonlinelink
from helpers import filehelper, urlhelper, csvhelper

import time
import os, random

import vlc
# import pafy
from sys import platform as PLATFORM

# eyeD3 import eyeD3
from configparser import ConfigParser
from tinytag import TinyTag


# import urllib
# from urllib.error import HTTPError
# import validators
# from validators import ValidationFailure
# import requests

def get_path_from_song_tag(tag):
    if tag.comment is None or tag.comment == '':
        return None
    for directory in videoFilePathSubDirectories:
        dir_name_to_check = directory.removeprefix(videoFilePath).replace("\\", '')
        if dir_name_to_check.lower() in tag.comment.lower() and len(tag.comment) >= 3:
            print('Tag Match for : ' + dir_name_to_check)
            return directory
    return None


# Return a row form the csv file based on an input
def find_track_in_sheet(tag):
    # Look through the dict for the song or it's tags
    # If a match return it's ind
    # If no match return -1
    print('Tag is: ' + str(tag))
    
    
    if tag.title is None or tag.title == '':
        return None
    for row in songList:
        if row["TRACKLIST_VALUE"].lower() in tag.title.lower():
            print('Song Match in Sheet for : ' + tag.title)
            return row
    return None


def new_song(most_recent_track_path):
    # Get the metadata of the most recent track, name, tags, etc
    tag = TinyTag.get(most_recent_track_path.strip())
    print(tag)
    exact_track_match = find_track_in_sheet(tag)
    tag_path = get_path_from_song_tag(tag)
    global current_file_path #todo make either a param or a class field
    if exact_track_match is not None:
        # TODO See if local path exists,

        if exact_track_match['LOCAL_PATH'] is not None:
            if filehelper.see_if_file_exists(exact_track_match['LOCAL_PATH']):
                current_file_path = exact_track_match["LOCAL_PATH"]
        elif exact_track_match['ONLINE_PATH'] is not None:
            # TODO Try to pull vid from online and DL to temp folder
            # See if in temp folder
            temp_file = filehelper.see_if_file_exists_in_tmp(videoFilePath)

            if temp_file:
                current_file_path = temp_file
            else:
                temp_file = dlonlinelink.try_get_link(videoFilePath)
                if temp_file:
                    current_file_path = temp_file
                else:
                    current_file_path = get_random_video_path(videoFilePath)

        else:
            current_file_path = get_random_video_path(videoFilePath)
    elif tag_path is not None:
        current_file_path = get_random_video_path(tag_path)

    else:
        # print("Track not found, displaying random video")
        print("In new song attempting to get file for the following: " + videoFilePath)
        current_file_path = get_random_video_path(videoFilePath)
    refresh_visuals()
    while media_list.count() > 1:
        media_list.remove_index(0)
        filehelper.clean_temp_folder(videoFilePath)
    return


def get_random_video_path(path_in):
    vid = random.choice(filehelper.get_all_file_paths_in_path(path_in))
    return vid


# Alwways a filepath
def refresh_visuals():
    global current_file_path #todo: can this become a parameter?
    # media_player.pause()
    print("REFRESHING VISUALS")
    # Validation if code is URL
    # if(urlhelper.is_path_url(current_file_path)):
    #    if(urlhelper.url_ok(current_file_path)):
    #        print("URL is OK")
    #    else:
    #        print("Bad URL, refreshing...")
    #        current_file_path = get_random_video_path(videoFilePath)
    #        refresh_visuals()
    media = None
    while media is None:
        try:
            media = instance.media_new(current_file_path)
        except:
            print("Failed to load media, refreshing...")
            current_file_path = get_random_video_path(videoFilePath)
    media_list.add_media(media)

    media_player.set_media_list(media_list)

    # code = media_player.play_item_at_index(0)
    code = media_player.next()
    # Can use this for debugging
    # TODO use defined values if they exist
    loop_start_time = 0
    loop_end_time = media_player.get_media_player().get_length() + 1000
    media_player.play()

    return

def main():
    # Load Config
    config = ConfigParser()
    config.read('config.ini')

    global videoFilePath
    videoFilePath = config['main_section'].get('videofolder_path')

    global videoFilePathSubDirectories
    videoFilePathSubDirectories = [f.path for f in os.scandir(videoFilePath) if f.is_dir()]
    # Load the csv into a dict
    global songList
    songList = csvhelper.csvtodict()

    # Get the latest m3u, aka history that VDJ is playing
    track_history_path = filehelper.get_latest_m3u(config['main_section'].get('dj_history_path'))

    # start VLC
    # ------------ Media Player Setup ---------#
    global instance
    global media_player
    global media_list
    global current_file_path

    instance = vlc.Instance()

    media_player = vlc.MediaListPlayer()
    media_list = instance.media_list_new()

    print("Video File Path is: " + videoFilePath)
    current_file_path = get_random_video_path(videoFilePath)
    print("Current file path is: " + current_file_path)
    # print(media_player.__dir__())
    print(media_list.__dir__())
    # print('Media List Count: ' + str(media_list.count()))
    # media = instance.media_new(current_file_path)
    # media_list.add_media(media)
    # media_player.set_media_list(media_list)

    media_player.set_playback_mode(vlc.PlaybackMode.loop)

    player = instance.media_player_new()
    player.audio_set_volume(0)
    player.set_fullscreen(True)
    media_player.set_media_player(player)
    # print(media_player.get_media())

    # player.playback_mode
    # list_player = inst.media_list_player_new()
    # media_list = inst.media_list_new([])
    # list_player.set_media_list(media_list)
    # player = list_player.get_media_player()

    global loop_start_time
    global loop_end_time
    # loop_start_time = 0
    # loop_end_time = media_player.get_media_player().get_length() + 1000
    most_recent_track_path = filehelper.read_last_line(track_history_path)
    print(most_recent_track_path)
    # time.sleep(1000)
    new_song(most_recent_track_path)
    #refresh_visuals()
    # refresh_visuals(current_file_path)

    # Waits for changes and does something when stuff changes
    # print(path)
    # print(last_update_time)
    # file = open(path)
    last_update_time = os.path.getmtime(track_history_path)
    while True:
        # print("See if new song")
        if last_update_time != os.path.getmtime(track_history_path):
            # Get most recently played track_history_path
            most_recent_track_path = filehelper.read_last_line(track_history_path)
            print(most_recent_track_path)
            last_update_time = os.path.getmtime(track_history_path)
            # time.sleep(1000)
            new_song(most_recent_track_path)

        # if(media_player.get_media_player().get_time() >=  loop_end_time):
        # print("Try Set Time")
        # print(loop_end_time)
        # print(media_player.get_media_player().get_length())
        # loop_end_time = player.get_length() - 100
        # media_player.get_media_player().set_time(loop_start_time)
        # player.set_position(0.0)
        # player.set_time(0)
        # player.play()
        # break
        # print(media_player.get_media_player().get_time())
        time.sleep(1)

        # player.pause()
        #

        # print(player.get_position())


if __name__ == "__main__":
    main()
