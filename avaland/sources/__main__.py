#!/usr/bin/env python

import argparse
from typing import List

from avaland import Music, Artist, Album
from avaland.manager import SourceManager
from avaland.sources import *

parser = argparse.ArgumentParser(description='Avaland Music Downloader')
parser.add_argument("query", type=str, help='search query')
parser.add_argument("--path", type=str, help='path to download')
parser.add_argument("--sources", type=str, help='list of sources (default: --sources all)\n'
                                                'available sources: bia2, next1, navahang, radiojavan, rapfarsi,'
                                                'wikiseda')

args = parser.parse_args()


def print_result(search_data):
    items = []
    musics = []  # type: List[Music]
    albums = []  # type: List[Album]
    artists = []  # type: List[Artist]
    counter = 1
    for source in search_data:
        musics.extend(search_data[source].musics)
        albums.extend(search_data[source].albums)
        artists.extend(search_data[source].artists)
    print("\nMusics:")
    if len(musics) == 0:
        print('\tNothing!')
    else:
        for music in musics:
            print("\t", "%s." % counter, "[%s]" % music.source.__site_name__, music.full_title)
            items.append(music)
            counter += 1
    print("\nAlbums:")
    if len(albums) == 0:
        print('\tNothing!')
    else:
        for album in albums:
            print("\t", "%s." % counter, "[%s]" % album.source.__site_name__, album.full_title)
            items.append(album)
            counter += 1
    print("\nArtists:")
    if len(artists) == 0:
        print('\tNothing!')
    else:
        for artist in artists:
            print("\t", "%s." % counter, "[%s]" % artist.source.__site_name__, artist.full_name)
            items.append(artist)
            counter += 1

    return items


def main():

    manager = SourceManager()
    manager.register(Bia2)
    manager.register(Nex1)
    manager.register(RapFarsi)
    manager.register(Navahang)
    manager.register(RadioJavan)
    manager.register(WikiSeda)
    search = manager.search(args.query)
    items = print_result(search)
    _input = input("Select an item to download (q for exit): ")
    if _input == "q":
        exit()
    while (not _input.isdigit()) or len(items) < int(_input) or int(_input) < 1:
        _input = input("(Invalid!) Select an item to download (q for exit): ")
        if _input == "q":
            exit()
    if type(items[int(_input) - 1]).__name__ != 'Music':
        print("Planned for future...")
        exit()

    items[int(_input) - 1].download(args.path)


if __name__ == '__main__':
    main()
