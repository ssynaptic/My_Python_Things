#!/data/data/com.termux/files/usr/bin/python3
from os import (environ,
                listdir)
from os.path import join
from subprocess import run
import sys
def main():
    print("Welcome to the terminal music player written in Python")
    print("Please select a song by ID:\n")
    music_folder = environ["MUSIC_FOLDER"]
    folder_content = listdir(music_folder)
    songs = {}
    for i in zip(range(1, len(folder_content)+1), folder_content):
        songs.update({i[0]:i[1]})
    while True:
        for i in songs.items():
            print(f"ID: {i[0]} - NAME: {i[1]}")
        user_option = int(input())
        if user_option in songs.keys():
            song = songs[user_option]
            print(f"Playing song: {user_option}")
            song_path = join(music_folder, song)
            run(["termux-media-player", "play", song_path])
            break
        else:
            print("Please select a valid song")
if __name__ == "__main__":
    try:
        main()
    except:
        print("An error has ocurred. Exiting...")