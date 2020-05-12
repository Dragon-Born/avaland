# -*- coding: utf-8 -*-

from xml.etree import ElementTree

import requests
from requests.exceptions import ConnectionError, HTTPError

from avaland.config import MAX_TIME_OUT
from avaland.data_types import Music, Artist, Album
from avaland.download import Download
from avaland.exceptions import SourceNetworkError, SourceException
from avaland.music_base import MusicBase
from avaland.search import SearchResult
from avaland.utils import test_attr


class Bia2(MusicBase):
    __site_name__ = 'Bia2'

    _search_url = "http://api.swiftype.com/api/v1/public/engines/search.json"
    _download_url = "http://cdn.biatik.com/api/android/2"
    _site_url = 'https://www.bia2.com/'
    _engine_key = "TxEmaszMvyJTZhnHaDBq"

    def __init__(self, config):
        MusicBase.__init__(self, config)

    @staticmethod
    def _reformat(text):
        return text.replace("on Bia2", "")

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
            res = requests.post(self._search_url,
                                data={"engine_key": self._engine_key, "q": query, "per_page": 50}, timeout=MAX_TIME_OUT)
        except ConnectionError:
            raise SourceNetworkError("Cannot connect to bia2music server.")
        except HTTPError:
            raise SourceNetworkError("Cannot connect to bia2music server. (HTTPError)")

        if res.status_code == 404:
            raise SearchResult(None, None, None)
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
                    Album(id=i["url"].split('/')[-1], title=self._reformat(title[0]), artist=self._reformat(title[1]),
                          url=i['url'], image=i['image'], source=Bia2))

        return SearchResult(musics, albums, artists)

    @test_attr(548)  # Helen
    def get_artist(self, artist_id):
        # type: (int) -> SearchResult
        url = self._download_url + '/artist.xml?id={}'.format(artist_id)
        try:
            res = requests.get(url, timeout=MAX_TIME_OUT)
        except ConnectionError:
            raise SourceNetworkError("Cannot connect to bia2music server.")
        except HTTPError:
            raise SourceNetworkError("Cannot connect to bia2music server. (HTTPError)")
        data = ElementTree.fromstring(res.content)[0]
        musics = []
        albums = []
        for i in range(len(data)):
            if data[i].tag == 'albums':
                for j in data[i]:
                    albums.append(
                        Album(id=int(j.get('id')), title=self._reformat(j.get('title')),
                              artist=self._reformat(data.get("name")), image=j.get('cover'), source=Bia2))

            if data[i].tag == 'singles':
                for j in data[i]:
                    musics.append(
                        Music(id=int(j.get('id')), title=self._reformat(j.get('title')), artist=data.get("name"),
                              url=data.get('share_url'), image=j.get('cover'), source=Bia2))
        return SearchResult(musics=musics, albums=albums, artists=[Artist(full_name=data.get("name"), id=artist_id,
                                                                          image=data.get("cover"), source=Bia2)])

    @test_attr(1267)  # Moon And Star - Helen
    def get_album(self, album_id):
        # type: (int) -> SearchResult
        url = self._download_url + '/album.xml?album={}'.format(album_id)
        try:
            res = requests.get(url, timeout=MAX_TIME_OUT)
        except ConnectionError:
            raise SourceNetworkError("Cannot connect to bia2music server.")
        except HTTPError:
            raise SourceNetworkError("Cannot connect to bia2music server. (HTTPError)")
        data = ElementTree.fromstring(res.content)[0]
        musics = []
        for i in data:
            musics.append(
                Music(id=int(i.get("id")), title=self._reformat(i.get("title")), artist=data.get('artist'),
                      url=data.get('share_url'), image=data.get('cover'), source=Bia2))
        return SearchResult(musics=musics)

    @test_attr(42271)  # Shomine - Helen
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

    def download(self, music_id, path=None):
        # type: (int, str) -> Download
        title, artist, url = self.get_download_url(music_id)
        download = Download(title, artist, url, path)
        download.get()
        return download
