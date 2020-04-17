from avaland.data_types import Music
from avaland.search import SearchResult
from avaland.download import Download


class MusicBase:
    __site_name__ = ''
    config = dict()
    testing = False

    def __init__(self, config):
        self.config = config

    def search(self, query: str) -> SearchResult:
        raise NotImplementedError

    def get_download_url(self, music: Music) -> str:
        raise NotImplementedError

    def download(self, music_id, path=None) -> Download:
        raise NotImplementedError
