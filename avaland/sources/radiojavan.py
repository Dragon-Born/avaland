# -*- coding: utf-8 -*-
from avaland.utils import test_attr

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote

import requests
from requests import HTTPError, ConnectionError

from avaland.config import MAX_TIME_OUT
from avaland.data_types import Music, Artist, Album
from avaland.download import Download
from avaland.exceptions import SourceNetworkError
from avaland.music_base import MusicBase
from avaland.search import SearchResult


class RadioJavan(MusicBase):
    __site_name__ = 'RadioJavan'

    _search_url = "https://api-rjvn.app/api2/search?query={query}"
    _download_url = "https://api-rjvn.app/api2/"
    _site_url = 'https://www.radiojavan.com'

    def __init__(self, config):
        MusicBase.__init__(self, config)

    @staticmethod
    def _reformat(text):
        return text

    @staticmethod
    def _split_album_title(title):
        if " by " in title:
            return title.split("by")
        if ' - ' in title:
            return title.split("-")
        return title, None

    @test_attr("hello")
    def search(self, query):
        # type: (str) -> SearchResult
        try:
            res = requests.get(self._search_url.format(query=quote(query)), timeout=MAX_TIME_OUT)
        except ConnectionError:
            raise SourceNetworkError("Cannot connect to RadioJavan server.")
        except HTTPError:
            raise SourceNetworkError("Cannot connect to RadioJavan server. (HTTPError)")
        data = res.json()
        musics = []
        albums = []
        artists = []
        if 'mp3s' in data:
            for i in data['mp3s']:
                musics.append(
                    Music(id=int(i["id"]), title=i['song'], artist=i['artist'], url=i['share_link'],
                          image=i['photo'], source=RadioJavan, download_url=i['link']))

        if 'artists' in data:
            for i in data['artists']:
                artists.append(
                    Artist(id=quote(i['name']), full_name=i['name'], image=i['photo'], source=RadioJavan))

        if 'albums' in data:
            for i in data['albums']:
                albums.append(
                    Album(id=int(i["id"]), title=self._reformat(i['album_album']),
                          artist=self._reformat(i['album_artist']), url=i['share_link'], image=i['photo'],
                          source=RadioJavan))

        return SearchResult(musics, albums, artists)

    @test_attr("Hichkas")  # Hichkas
    def get_artist(self, artist_id):
        # type: (str) -> SearchResult
        try:
            res = requests.get(self._download_url + "artist?query={id}".format(id=artist_id), timeout=MAX_TIME_OUT)
        except ConnectionError:
            raise SourceNetworkError("Cannot connect to Next1 server.")
        except HTTPError:
            raise SourceNetworkError("Cannot connect to Next1 server. (HTTPError)")
        musics = []
        albums = []
        data = res.json()
        if 'mp3s' in data:
            for i in data['mp3s']:
                musics.append(
                    Music(id=int(i["id"]), title=i['song'], artist=i['artist'], url=i['share_link'],
                          image=i['photo'], source=RadioJavan, download_url=i['link']))

        if 'albums' in data:
            for i in data['albums']:
                albums.append(
                    Album(id=int(i["album_id"]), title=self._reformat(i['album_album']),
                          artist=self._reformat(i['album_artist']), url=i['album']['share_link'], image=i['photo'],
                          source=RadioJavan))

        return SearchResult(musics=musics, albums=albums, artists=[Artist(full_name=data['query'], id=artist_id, source=RadioJavan)])

    @test_attr(44893)  # Jangale Asfalt - Hichkas
    def get_album(self, album_id):
        # type: (int) -> SearchResult
        try:
            res = requests.get(self._download_url + "mp3?id={id}".format(id=album_id), timeout=MAX_TIME_OUT)
        except ConnectionError:
            raise SourceNetworkError("Cannot connect to Next1 server.")
        except HTTPError:
            raise SourceNetworkError("Cannot connect to Next1 server. (HTTPError)")
        musics = []
        data = res.json()
        albums = []
        artist = [Artist(full_name=data['artist'], id=quote(data['artist']).lower())]
        if 'album_tracks' in data:
            albums.append(Album(artist=data['album_artist'], title=data['album_album']))
            for i in data['album_tracks']:
                if i['type'] == 'mp3':
                    musics.append(
                        Music(id=i['id'], title=self._reformat(i['song']), artist=i['artist'],
                              url=i['share_link'], image=i["photo"], source=RadioJavan, download_link=i['link']))
        else:
            if data['type'] == 'mp3':
                musics.append(
                    Music(id=data['id'], title=self._reformat(data['song']), artist=data['artist'],
                          url=data['share_link'], image=data["photo"], source=RadioJavan, download_link=data['link']))
        return SearchResult(musics=musics, albums=albums, artists=artist)

    @test_attr(88782)  # Hich - Reza Bahram
    def get_download_url(self, music_id):
        url = self._download_url + "mp3?id={id}".format(id=music_id)
        try:
            res = requests.get(url, timeout=MAX_TIME_OUT)
        except ConnectionError:
            raise SourceNetworkError("Cannot connect to RadioJavan server.")
        except HTTPError:
            raise SourceNetworkError("Cannot connect to RadioJavan server. (HTTPError)")
        data = res.json()
        return data.get('song'), data.get('artist'), data.get('link')

    def download(self, music_id, path=None):
        # type: (int, str) -> Download
        title, artist, url = self.get_download_url(music_id)
        download = Download(title, artist, url, path)
        download.get()
        return download
