import requests
from xml.etree import ElementTree
from avaland.config import MAX_TIME_OUT
from avaland.data_types import Music, Artist, Album
from avaland.download import Download
from avaland.music_base import MusicBase
from avaland.search import SearchResult
from requests.exceptions import ConnectionError, HTTPError
from avaland.exceptions import SourceNetworkError


class Bia2(MusicBase):
    __site_name__ = 'bia2'

    _search_url = "http://api.swiftype.com/api/v1/public/engines/search.json"
    _download_url = "http://cdn.biatik.com/api/android/2"
    _site_url = 'https://www.bia2.com/'
    _engine_key = "TxEmaszMvyJTZhnHaDBq"

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
            res = requests.post(self._search_url,
                                data={"engine_key": self._engine_key, "q": query, "per_page": 50}, timeout=MAX_TIME_OUT)
        except ConnectionError:
            raise SourceNetworkError("Cannot connect to bia2music server.")
        except HTTPError:
            raise SourceNetworkError("Cannot connect to bia2music server. (HTTPError)")

        if res.status_code == 404:
            pass  # TODO: get new engine key
        data = res.json()['records']['page']
        musics = []
        albums = []
        artists = []
        for i in data:
            if i['type'] == 'music':
                musics.append(
                    Music(id=i["music_id"], title=self._reformat(i['title']), artist=i['artist'], url=i['url'],
                          image=i['image'], source=Bia2))
            elif i['type'] == 'artist':
                artists.append(
                    Artist(id=i["artist_id"], full_name=i['title'], url=i['url'], image=i['image'], source=Bia2))
            elif i['type'] == '':
                title = self._split_album_title(i['title'])

                albums.append(
                    Album(id=i["id"], title=self._reformat(title[0]), artist=self._reformat(title[1]),
                          url=i['url'], image=i['image'], source=Bia2))

        return SearchResult(musics, albums, artists)

    def get_download_url(self, music_id):
        url = self._download_url + '/music.xml?id={}'.format(music_id)
        try:
            res = requests.get(url, timeout=MAX_TIME_OUT)
        except ConnectionError:
            raise SourceNetworkError("Cannot connect to bia2music server.")
        except HTTPError:
            raise SourceNetworkError("Cannot connect to bia2music server. (HTTPError)")
        data = ElementTree.fromstring(res.content)[0]
        return data.get('Title'), data.get('Artist'), data.get('mp3')

    def download(self, music_id, path=None) -> Download:
        title, artist, url = self.get_download_url(music_id)
        download = Download(title, artist, url, path)
        download.get()
        return download
