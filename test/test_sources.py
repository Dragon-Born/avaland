import inspect
import unittest

from avaland import sources
from avaland import MusicBase
from avaland.search import SearchResult


def test_search(self):
    query = self.source.search.test
    source = self.source({}).search(query)
    self.assertIsInstance(source, SearchResult)


def test_artist_id(self):
    artist = self.source.get_artist.test
    source = self.source({}).get_artist(artist)
    self.assertIsInstance(source, SearchResult)


def test_album_id(self):
    album = self.source.get_album.test
    source = self.source({}).get_album(album)
    self.assertIsInstance(source, SearchResult)


def test_download_url(self):
    music_id = self.source.get_download_url.test
    data = self.source({}).get_download_url(music_id)
    self.assertEqual(len(data), 3)


def _create_class(name, obj):
    _class = type(name + "Test", (unittest.TestCase,), {
        "source": obj,
        "test_search": test_search,
        "test_artist": test_artist_id,
        "test_album": test_album_id,
        "test_download": test_download_url
    })
    return _class


class_members = inspect.getmembers(sources, inspect.isclass)

for i in class_members:
    if issubclass(i[1], MusicBase) and i[1] != MusicBase:
        globals()[i[0]] = _create_class(i[0], i[1])


