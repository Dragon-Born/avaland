from urllib.parse import quote

import requests

from requests import HTTPError

from avaland.config import MAX_TIME_OUT
from avaland.data_types import Music, Artist, Album
from avaland.download import Download
from avaland.exceptions import SourceNetworkError
from avaland.music_base import MusicBase
from avaland.search import SearchResult


class WikiSeda(MusicBase):

    __site_name__ = 'wikiseda'

    _search_url = "http://www.getsongg.com/dapp/?order=top&type=all&page=1&query={query}&lang=en&v=70022"
    _download_url = "http://www.getsongg.com/dapp/gettrackdetail?id={id}&lang=en"
    _site_url = 'https://www.wikiseda.com/'

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
            res = requests.post(self._search_url.format(query=quote(query)), timeout=MAX_TIME_OUT)
        except ConnectionError:
            raise SourceNetworkError("Cannot connect to WikiSeda server.")
        except HTTPError:
            raise SourceNetworkError("Cannot connect to WikiSeda server. (HTTPError)")
        data = res.json()
        musics = []
        albums = []
        artists = []
        for i in data:
            if i['type'] == 'song':
                musics.append(
                    Music(id=int(i["id"]), title=self._reformat(i['songname']), artist=i['artist'], url=i['url'],
                          image=i['poster'], source=WikiSeda))
            elif i['type'] == 'artist':
                artists.append(
                    Artist(id=int(i["id"]), full_name=i['artist'], url=i['url'], image=i['poster'], source=WikiSeda))
            elif i['type'] == 'album':
                albums.append(
                    Album(id=i["id"], title=self._reformat(i['album']), artist=self._reformat(i['artist']),
                          url=i['url'], image=i['poster'], source=WikiSeda))

        return SearchResult(musics, albums, artists)

    def get_download_url(self, music_id):
        url = self._download_url.format(id=music_id)
        try:
            res = requests.get(url, timeout=MAX_TIME_OUT)
        except ConnectionError:
            raise SourceNetworkError("Cannot connect to WikiSeda server.")
        except HTTPError:
            raise SourceNetworkError("Cannot connect to WikiSeda server. (HTTPError)")
        data = res.json()['song'][0]
        return data.get('songname'), data.get('artist'), data.get('mp3')

    def download(self, music_id, path=None) -> Download:
        title, artist, url = self.get_download_url(music_id)
        download = Download(title, artist, url, path)
        download.get()
        return download
