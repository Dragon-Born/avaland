import requests
from requests import HTTPError

from avaland.config import MAX_TIME_OUT
from avaland.data_types import Music, Album
from avaland.download import Download
from avaland.exceptions import SourceNetworkError
from avaland.music_base import MusicBase
from avaland.search import SearchResult
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Nex1(MusicBase):
    __site_name__ = 'nex1music'

    _search_url = "https://apin1mservice.com/WebService/search.php"
    _download_url = "https://apin1mservice.com/WebService/music-more.php"
    _site_url = 'https://nex1music.ir'

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

    def download(self, music_id, path=None) -> Download:
        title, artist, url = self.get_download_url(music_id)
        download = Download(title, artist, url, path)
        download.get()
        return download
