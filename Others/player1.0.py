# A very simple music player for Termux
# This is a proof
from os.path import join, dirname
from os import listdir, system
from subprocess import run
from time import sleep
import sys, re

current_path = dirname(__file__)
music_path = join(current_path, "music")

def get_files():
    global music_path
    for i in listdir(music_path):
        yield i

def get_songs():
    global music_path
    files = get_files()
    songs_names = []
    songs = {}
    while True:
        try:
            file = next(files)
            songs_names.append(file)
        except:
            break
    for x, y in zip(range(1, len(songs_names)+1), songs_names):
        songs.update({x:y})
    print("Select A Song:")
    for x, y in songs.items():
        print(x, "-", y.replace(".mp3", ""))
    user_song = input()
    valid_song = 0
    if not user_song:
        print("[-] No song selected exiting...")
        sys.exit()
    else:
        for i in songs.keys():
            if int(user_song) == i:
                valid_song += 1
    if valid_song:
        s = songs[int(user_song)]
        print("You selected the song", s.replace(".mp3", ""))
        run(["termux-media-player", "play", join(music_path, s)])

if __name__ == "__main__":
    get_songs()
