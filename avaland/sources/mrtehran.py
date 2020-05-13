# -*- coding: utf-8 -*-
import requests
import urllib3
from avaland.config import MAX_TIME_OUT
from avaland.data_types import Album, Artist, Music
from avaland.download import Download
from avaland.exceptions import SourceNetworkError
from avaland.music_base import MusicBase
from avaland.search import SearchResult
from avaland.utils import test_attr
from bs4 import BeautifulSoup
from requests import ConnectionError, HTTPError

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class MrTehran(MusicBase):
    __site_name__ = 'MrTehran'

    _download_url = "https://cdnmrtehran.ir/media/"
    _api_url = "http://mrtehran.net/mt-app/v506/"
    _site_url = 'https://www.mrtehran.com'

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
            res_tracks = requests.post(self._api_url + "main_search_tracks.php", data={"search_text":query, "page":0, "is_iran":1}, timeout=MAX_TIME_OUT)
            res_albums = requests.post(self._api_url + "main_search_albums.php", data={"search_text":query, "page":0, "is_iran":1}, timeout=MAX_TIME_OUT)
            res_artists = requests.post(self._api_url + "main_search_artists.php", data={"search_text":query, "page":0}, timeout=MAX_TIME_OUT)
        except ConnectionError:
            raise SourceNetworkError("Cannot connect to MrTehran server.")
        except HTTPError:
            raise SourceNetworkError("Cannot connect to MrTehran server. (HTTPError)")

        data_tracks = res_tracks.json()
        data_albums = res_albums.json()
        data_artists = res_artists.json()

        musics = []
        albums = []
        artists = []
        for i in data_tracks:
            musics.append(
                Music(id=int(i["track_id"]), title=self._reformat(i["track_title"]), artist=i["track_artist"], url=self._download_url + i["track_audio"],
                        image=self._download_url + i["track_thumbnail"], source=MrTehran))

        for i in data_artists:
            image = None
            if not i["artist_thumbnail"] is None:
                image = self._download_url + i["artist_thumbnail"]
            artists.append(
                Artist(id=int(i["artist_id"]), full_name=i["artist_name"], url=self._site_url + "artist/" + i["artist_id"], image=image,
                        source=MrTehran))

        for i in data_albums:
            image = None
            if not i["track_artwork"] is None:
                image = self._download_url + i["track_artwork"]
            albums.append(
                Album(id=int(i["album_id"]), title=self._reformat(i["album_title"]), artist=self._reformat(i["album_artist"]),
                        url=(self._site_url + "mp3/" + i["track_id"] + "/" + i["track_artist"] + "/" + i["track_title"]).lower().replace(" ","-"), image=image, source=MrTehran))

        return SearchResult(musics, albums, artists)

    @test_attr(57)  # Shadmehr Aghili
    def get_artist(self, artist_id):
        try:
            res = requests.post(self._api_url + "artist_data.php", data={"user_id":217604, "artist_id":artist_id, "is_iran":1}, timeout=MAX_TIME_OUT)
        except ConnectionError:
            raise SourceNetworkError("Cannot connect to MrTehran server.")
        except HTTPError:
            raise SourceNetworkError("Cannot connect to MrTehran server. (HTTPError)")
        musics = []
        albums = []
        data = res.json()
        for i in data['all_tracks']:
            musics.append(
                Music(id=int(i["track_id"]), title=self._reformat(i["track_title"]), artist=i["track_artist"], url=self._download_url + i["track_audio"],
                        image=self._download_url + i["track_thumbnail"], source=MrTehran))
        for i in data['all_albums']:
            image = None
            if not i["track_artwork"] is None:
                image = self._download_url + i["track_artwork"]
            albums.append(
                Album(id=int(i["album_id"]), title=self._reformat(i["album_title"]), artist=i["album_artist"], url=(self._site_url + "mp3/" + i["track_id"] + "/" + i["track_artist"] + "/" + i["track_title"]).lower().replace(" ","-"),
                        image=image, source=MrTehran))
        return SearchResult(musics=musics, albums=albums, artists=[Artist(full_name=data.get('artist_info').get('artist_name'), id=data.get('artist_info').get('artist_id'), source=MrTehran)])

    def get_related_tracks(self, track_id, album_id=0):
        try:
            res = requests.post(self._api_url + "related_tracks.php", data={"track_id":track_id, "album_id":album_id, "is_iran":1}, timeout=MAX_TIME_OUT)
        except ConnectionError:
            raise SourceNetworkError("Cannot connect to MrTehran server.")
        except HTTPError:
            raise SourceNetworkError("Cannot connect to MrTehran server. (HTTPError)")
        data = res.json()
        return data

    @test_attr(409)  # Shadmehr Aghili - Pare Parvaz
    def get_album(self, album_id):
        # type: (str) -> SearchResult
        datas = self.get_related_tracks(0, album_id)
        musics = []
        for i in datas:
            if i["album_id"] == album_id:
                musics.append(Music(id=int(i["track_id"]), title=self._reformat(i["track_title"]), artist=i["track_artist"], url=self._download_url + i["track_audio"],
                        image=self._download_url + i["track_thumbnail"], source=MrTehran))
        return SearchResult(musics=musics)

    @test_attr(198177)  # Arash - Dooset Daram (Ft. Helena)
    def get_download_url(self, music_id):
        data = self.get_related_tracks(music_id)
        datas = self.get_related_tracks(data[0]["track_id"])
        result = {}
        for i in datas:
            if i["track_id"] == music_id:
                result["title"] = self._reformat(i["track_title"])
                result["artist"] = i["track_artist"]
                result["download_url"] = self._download_url + i["track_audio"]
        return result.get('title'), result.get('artist'), result.get('download_url')

    def download(self, music_id, path=None):
        # type: (int, str) -> Download
        title, artist, url = self.get_download_url(music_id)
        download = Download(title, artist, url, path)
        download.get()
        return download
