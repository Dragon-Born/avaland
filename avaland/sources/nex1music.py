# -*- coding: utf-8 -*-
import json

import requests
import urllib3
from requests import HTTPError, ConnectionError

from avaland.config import MAX_TIME_OUT
from avaland.data_types import Music, Album
from avaland.download import Download
from avaland.exceptions import SourceNetworkError
from avaland.music_base import MusicBase
from avaland.search import SearchResult
from avaland.utils import test_attr

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Nex1(MusicBase):
    __site_name__ = 'Nex1Music'

    _search_url = "https://apin1mservice.com/WebService/search.php"
    _download_url = "https://apin1mservice.com/WebService/music-more.php"
    _site_url = 'https://nex1music.ir'

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
            res = requests.post(self._search_url, data={"text": query}, timeout=MAX_TIME_OUT)
        except ConnectionError:
            raise SourceNetworkError("Cannot connect to Nex1 Music server.")
        except HTTPError:
            raise SourceNetworkError("Cannot connect to Nex1 Music server. (HTTPError)")
        data = res.json()
        musics = []
        albums = []
        artists = []
        for i in data:
            if 'type' in i and i['type'] == 'تک آهنگ':
                musics.append(
                    Music(id=int(i["id"]), title=self._reformat(i['tracken']), artist=i['artisten'], url=None,
                          image=i['image'], source=Nex1))

            elif 'type' in i and i['type'] == 'آلبوم':
                albums.append(
                    Album(id=i["id"], title=self._reformat(i['tracken']), artist=self._reformat(i['artisten']),
                          url=None, image=i['image'], source=Nex1))

        return SearchResult(musics, albums, artists)

    @test_attr(12715)  # Hel Hele - Amir Masih
    def get_download_url(self, music_id):
        url = self._download_url
        try:
            res = requests.post(url, data={"post_id": music_id}, timeout=MAX_TIME_OUT)
        except ConnectionError:
            raise SourceNetworkError("Cannot connect to Nex1 Music server.")
        except HTTPError:
            raise SourceNetworkError("Cannot connect to Nex1 Music server. (HTTPError)")
        data = res.json()
        return data.get('TrackEn'), data.get('ArtistEn'), data.get('Music320')

    @test_attr(0)  # nothing!
    def get_artist(self, artist_id):
        return SearchResult(None, None, None)

    @test_attr(12792)  # Mojaz - Hichkas
    def get_album(self, album_id):
        # type: (str) -> SearchResult
        try:
            res = requests.post(self._download_url, data={"post_id": album_id}, timeout=MAX_TIME_OUT)
        except ConnectionError:
            raise SourceNetworkError("Cannot connect to Next1 server.")
        except HTTPError:
            raise SourceNetworkError("Cannot connect to Next1 server. (HTTPError)")
        musics = []
        data = json.loads(res.json()['AlbumTrackList'])
        for i in data:
            musics.append(
                Music(id=None, title=self._reformat(i['album_track_name_en']), artist=res.json()["ArtistEn"],
                      url=res.json()['PostUrl'], image=res.json()["Image"], source=Nex1,
                      download_url=i['album_track_link_320']))
        return SearchResult(musics=musics)

    def download(self, music_id, path=None):
        # type: (int, str) -> Download
        title, artist, url = self.get_download_url(music_id)
        download = Download(title, artist, url, path)
        download.get()
        return download
