from urllib.parse import quote

import requests
import urllib3
from requests import HTTPError

from avaland.config import MAX_TIME_OUT
from avaland.data_types import Music, Artist, Album
from avaland.download import Download
from avaland.exceptions import SourceNetworkError
from avaland.music_base import MusicBase
from avaland.search import SearchResult

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Navahang(MusicBase):
    __site_name__ = 'navahang'
    _search_url = "https://navahang.com/main-search.php?q={query}&size=50"
    _download_url = "https://173.236.47.154/webservice/GetSingleMediaInfo?media_id={id}"
    _site_url = 'https://www.navahang.com'

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
            raise SourceNetworkError("Cannot connect to Navahang server.")
        except HTTPError:
            raise SourceNetworkError("Cannot connect to Navahang server. (HTTPError)")

        data = res.json()

        musics = []
        albums = []
        artists = []
        if 'MP3' in data:
            for i in data['MP3']:
                title, artist = i['title'].split(' – ')
                musics.append(
                    Music(id=int(i["id"]), title=self._reformat(title), artist=artist, url=self._site_url + i['url'],
                          image=i['image'], source=Navahang))

        if 'Artist' in data:
            for i in data['Artist']:
                artists.append(
                    Artist(id=int(i["id"]), full_name=i['title'], url=self._site_url + i['url'], image=i['image'],
                           source=Navahang))

        if 'Album' in data:
            for i in data['Album']:
                album, artist = i['title'].split(' – ')
                albums.append(
                    Album(id=int(i["id"]), title=self._reformat(album), artist=self._reformat(artist),
                          url=self._site_url + i['url'], image=i['image'], source=Navahang))

        return SearchResult(musics, albums, artists)

    def get_download_url(self, music_id):
        url = self._download_url.format(id=music_id)
        try:
            res = requests.get(url, verify=False, timeout=MAX_TIME_OUT)
        except ConnectionError:
            raise SourceNetworkError("Cannot connect to Navahang server.")
        except HTTPError:
            raise SourceNetworkError("Cannot connect to Navahang server. (HTTPError)")
        data = res.json()[0]
        return data.get('song_name'), data.get('artist_name'), data.get('download')

    def download(self, music_id, path=None) -> Download:
        title, artist, url = self.get_download_url(music_id)
        download = Download(title, artist, url, path)
        download.get()
        return download
