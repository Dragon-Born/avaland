from urllib.parse import quote

import requests
from requests import HTTPError

from avaland.config import MAX_TIME_OUT
from avaland.data_types import Music, Artist, Album
from avaland.download import Download
from avaland.exceptions import SourceNetworkError
from avaland.music_base import MusicBase
from avaland.search import SearchResult


class RadioJavan(MusicBase):
    __site_name__ = 'RadioJavan'

    _search_url = "https://api-rjvn.app/api2/search?query={query}"
    _download_url = "https://api-rjvn.app/api2/mp3?id={id}"
    _site_url = 'https://www.radiojavan.com'

    def __init__(self, config):
        super().__init__(config)

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

    def search(self, query) -> SearchResult:
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
                    Artist(id=None, full_name=i['name'], image=i['photo'], source=RadioJavan))

        if 'albums' in data:
            for i in data['albums']:
                print(self._reformat(i['album']))
                albums.append(
                    Album(id=int(i["id"]), title=self._reformat(i['album']), artist=self._reformat(i['artist']),
                          url=i['share_link'], image=i['photo'], source=RadioJavan))

        return SearchResult(musics, albums, artists)

    def get_download_url(self, music_id):
        url = self._download_url.format(id=music_id)
        try:
            res = requests.get(url, timeout=MAX_TIME_OUT)
        except ConnectionError:
            raise SourceNetworkError("Cannot connect to RadioJavan server.")
        except HTTPError:
            raise SourceNetworkError("Cannot connect to RadioJavan server. (HTTPError)")
        data = res.json()
        return data.get('song'), data.get('artist'), data.get('link')

    def download(self, music_id, path=None) -> Download:
        title, artist, url = self.get_download_url(music_id)
        download = Download(title, artist, url, path)
        download.get()
        return download
