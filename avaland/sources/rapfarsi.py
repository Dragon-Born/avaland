# -*- coding: utf-8 -*-
from avaland.utils import test_attr

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote

import requests
from requests import HTTPError, ConnectionError

from avaland.config import MAX_TIME_OUT
from avaland.data_types import Music, Album
from avaland.download import Download
from avaland.exceptions import SourceNetworkError
from avaland.music_base import MusicBase
from avaland.search import SearchResult


class RapFarsi(MusicBase):
    __site_name__ = 'RapFarsi'

    _search_url = "http://51.89.98.91:3004/S/search/{query}"

    _headers = {"User-Agent": "okhttp/3.4.1",
                "Accept-Encoding": "gzip",
                "Content-Type": "application/x-www-form-urlencoded"}

    _download_url = "http://51.89.98.91:3004/S/{id}"
    _site_url = 'https://www.rapfarsi.co'

    def __init__(self, config):
        MusicBase.__init__(self, config)

    @staticmethod
    def _reformat(text):
        return text

    @test_attr("hello")
    def search(self, query):
        # type: (str) -> SearchResult
        try:
            res = requests.post(self._search_url.format(query=quote(query)), headers=self._headers,
                                timeout=MAX_TIME_OUT)
        except ConnectionError:
            raise SourceNetworkError("Cannot connect to RapFarsi server.")
        except HTTPError:
            raise SourceNetworkError("Cannot connect to RapFarsi server. (HTTPError)")
        data = res.json()
        musics = []
        albums = []
        artists = []
        for i in data:
            if i['type'] == 'single':
                musics.append(Music(id=i["slug"], title=self._reformat(i['title']), artist=i['artistTitle'],
                                    url=self._site_url + i['link'], image=i['cover']['full'], source=RapFarsi,
                                    download_link=i['track320']['link'] if i['track320'] else i['track128']['link'] if
                                    'track128' in i and i['track128'] else None))
            elif i['type'] == 'album':
                albums.append(
                    Album(id=i["slug"], title=self._reformat(i['title']), artist=self._reformat(i['artistTitle']),
                          url=self._site_url + i['link'], image=i['cover']['full'], source=RapFarsi))

        return SearchResult(musics, albums, artists)

    @test_attr("hichkas-dastasho-mosht-karde")  # Dastasho Mosht Karde - Hichkas
    def get_download_url(self, music_id):
        url = self._download_url.format(id=music_id)
        try:
            res = requests.post(url, headers=self._headers, timeout=MAX_TIME_OUT)
        except ConnectionError:
            raise SourceNetworkError("Cannot connect to RapFarsi server.")
        except HTTPError:
            raise SourceNetworkError("Cannot connect to RapFarsi server. (HTTPError)")
        data = res.json()['Post']
        return data.get('title'), data.get('artistTitle'), data['track320']['link']

    @test_attr(0)  # nothing!
    def get_artist(self, artist_id):
        return SearchResult(None, None, None)

    @test_attr("hichkas-mojaz")  # Mojaz - Hichkas
    def get_album(self, album_id):
        # type: (str) -> SearchResult
        try:
            res = requests.post(self._download_url.format(id=album_id), timeout=MAX_TIME_OUT)
        except ConnectionError:
            raise SourceNetworkError("Cannot connect to Next1 server.")
        except HTTPError:
            raise SourceNetworkError("Cannot connect to Next1 server. (HTTPError)")
        musics = []
        data = res.json()['Post']
        for i in data['albumList']:
            artist, title = data['artistTitle'], i['title']
            musics.append(
                Music(id=i['id'], title=self._reformat(title), artist=artist, url=self._site_url + data['link'],
                      image=i["cover"]['full'], source=RapFarsi,
                      download_link=i['track320']['link'] if i['track320'] else i['track128']['link']))
        return SearchResult(musics=musics)

    def download(self, music_id, path=None):
        # type: (int, str) -> Download
        title, artist, url = self.get_download_url(music_id)
        download = Download(title, artist, url, path)
        download.get()
        return download
