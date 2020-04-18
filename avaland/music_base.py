from avaland.data_types import Music
from avaland.download import Download
from avaland.search import SearchResult


class MusicBase(object):
    __site_name__ = ''
    config = dict()
    testing = False

    def __init__(self, config):
        self.config = config

    def search(self, query):
        # type: (str) -> SearchResult
        raise NotImplementedError

    def get_artist(self, artist_id):
        # type: (str) -> SearchResult
        raise NotImplementedError

    def get_album(self, album_id):
        # type: (str) -> SearchResult
        raise NotImplementedError

    def get_download_url(self, music):
        # type: (Music) -> str
        raise NotImplementedError

    def download(self, music_id, path=None):
        # type: (int, str) -> Download
        raise NotImplementedError
