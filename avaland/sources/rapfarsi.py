from urllib.parse import quote

import requests
from requests import HTTPError

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
        super().__init__(config)

    @staticmethod
    def _reformat(text):
        return text

    def search(self, query) -> SearchResult:
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
                                    url=self._site_url + i['link'], image=i['cover']['full'], source=RapFarsi))
            elif i['type'] == 'album':
                albums.append(
                    Album(id=i["slug"], title=self._reformat(i['title']), artist=self._reformat(i['artistTitle']),
                          url=self._site_url + i['link'], image=i['cover']['full'], source=RapFarsi))

        return SearchResult(musics, albums, artists)

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

    def download(self, music_id, path=None) -> Download:
        title, artist, url = self.get_download_url(music_id)
        download = Download(title, artist, url, path)
        download.get()
        return download
