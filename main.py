import os

import eyed3
from eyed3.core import AudioFile
from ytmusicapi import YTMusic


def writeMusicToFile(audiofiles: [AudioFile]):
    with open('outputpy.txt', 'a', encoding='utf-8') as f:
        for file in audiofiles:
            f.write(f"{file.tag.artist} - {file.tag.title}\n")


def addMusicToYtMusic(playlistName: str, playlistDescription: str, audiofiles: [AudioFile]):
    client = YTMusic('headers_auth.json')
    playlistId = client.create_playlist(playlistName, playlistDescription)
    failedTracks = []
    print("Started adding music to YouTube Music")
    i = 1
    progress = 0
    step = 100 / len(tracksWithTags)

    for file in audiofiles:
        searchResults = list(filter(lambda r: (r['resultType'] == 'song'), client.search(f"{file.tag.artist} - {file.tag.title}")))
        if len(searchResults) > 0:
            client.add_playlist_items(playlistId, [searchResults[0]['videoId']])
            print('\033[96m' + f"{file.tag.artist} - {file.tag.title} added to {playlistName} || {i} of {len(tracksWithTags)} - {round(progress, 2)}%")
        else:
            failedTracks.append(f"{file.tag.artist} - {file.tag.title}")
            print('\033[93m' + f"{file.tag.artist} - {file.tag.title} not found! || {i} of {len(tracksWithTags)} - {round(progress, 2)}%")
        progress = progress + step
        i = i + 1
    print("Finished adding music to YouTube Music")
    if len(failedTracks) > 0:
        [print('\033[93m' + fail, sep='\n') for fail in failedTracks]


def getTags(dirPath: str):
    eyed3.log.setLevel("ERROR")
    files = os.listdir(dirPath)
    tags = []

    i = 0
    progress = 0
    step = 100 / len(files)
    print("Starting getting tags")

    for file in files:
        tags.append(eyed3.load(f"{dirPath}\\{file}"))
        progress = progress + step
        i = i + 1
        if i % 100 == 0:
            print(f"{round(progress, 2)}%")

    print("Finishing getting tags")
    return tags


if __name__ == '__main__':
    tracksWithTags = getTags("E:\\Music")
    # writeMusicToFile(tracksWithTags)
    addMusicToYtMusic("Legacy2", "Testing method", tracksWithTags)



