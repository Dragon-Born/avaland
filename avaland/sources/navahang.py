# -*- coding: utf-8 -*-
from avaland.utils import test_attr

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote

import requests
import urllib3
from requests import HTTPError, ConnectionError

from avaland.config import MAX_TIME_OUT
from avaland.data_types import Music, Artist, Album
from avaland.download import Download
from avaland.exceptions import SourceNetworkError
from avaland.music_base import MusicBase
from avaland.search import SearchResult

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Navahang(MusicBase):
    __site_name__ = 'Navahang'
    _search_url = "https://navahang.com/main-search.php?q={query}&size=50"
    _api_url = "https://navahang.co/navaapi2/"
    _site_url = 'https://www.navahang.com'

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
                try:
                    album, artist = i['title'].split(' – ')
                except:
                    album, artist = i['title'], None
                albums.append(
                    Album(id=int(i["id"]), title=self._reformat(album), artist=self._reformat(artist),
                          url=self._site_url + i['url'], image=i['image'], source=Navahang))

        return SearchResult(musics, albums, artists)

    @test_attr(630620)  # Helen
    def get_artist(self, artist_id):
        url = self._api_url + "GetArtistById?id={id}".format(id=artist_id)
        try:
            res = requests.get(url, timeout=MAX_TIME_OUT)
        except ConnectionError:
            raise SourceNetworkError("Cannot connect to Navahang server.")
        except HTTPError:
            raise SourceNetworkError("Cannot connect to Navahang server. (HTTPError)")
        musics = []
        albums = []
        data = res.json()
        for i in data['works']:
            if i['category'] == 'MP3':
                musics.append(
                    Music(id=i["post_id"], title=self._reformat(i['song_name']), artist=i['artist_name'],
                          image=i['image'], source=Navahang, download_url=i['high_quality']))
            elif i['category'] == 'Album':
                albums.append(
                    Music(id=i["albumId"], title=self._reformat(i['song']), artist=i['artist'],
                          image=i['playerimage'], source=Navahang))
        return SearchResult(musics=musics, albums=albums, artists=[Artist(full_name=data['name'], id=artist_id, source=Navahang)])

    @test_attr(171108)  # Helen - Negahe To
    def get_album(self, album_id):
        # type: (str) -> SearchResult
        url = self._api_url + "GetPlaylistSongs?playlistId={id}".format(id=album_id)
        try:
            res = requests.get(url, timeout=MAX_TIME_OUT)
        except ConnectionError:
            raise SourceNetworkError("Cannot connect to Navahang server.")
        except HTTPError:
            raise SourceNetworkError("Cannot connect to Navahang server. (HTTPError)")
        musics = []
        data = res.json()['SONG_LIST']
        for i in data:
            musics.append(
                Music(id=i["post_id"], title=self._reformat(i['song_name']), artist=i['artist_name'],
                      url=res.json()['SHARE_LINK']['link'], image=i['image_Mp3'], source=Navahang))
        return SearchResult(musics=musics)

    @test_attr(198177)  # Arash - Dooset Daram (Ft. Helena)
    def get_download_url(self, music_id):
        url = self._api_url + "GetSingleMediaInfo?media_id={id}".format(id=music_id)
        try:
            res = requests.get(url, timeout=MAX_TIME_OUT)
        except ConnectionError:
            raise SourceNetworkError("Cannot connect to Navahang server.")
        except HTTPError:
            raise SourceNetworkError("Cannot connect to Navahang server. (HTTPError)")
        data = res.json()[0]
        return data.get('song_name'), data.get('artist_name'), data.get('download')

    def download(self, music_id, path=None):
        # type: (int, str) -> Download
        title, artist, url = self.get_download_url(music_id)
        download = Download(title, artist, url, path)
        download.get()
        return download
