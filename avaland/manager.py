import traceback
from typing import Type, Dict

from avaland.exceptions import AvalandException, SourceNotRegisteredException
from avaland.music_base import MusicBase
from avaland.search import SearchResult


class SourceManager:
    _config = dict()
    _sources = dict()

    def register(self, source: Type[MusicBase], config=None):
        if config is None:
            config = {}
        self._sources[source.__site_name__] = source
        self._config[source.__site_name__] = config
        return self

    def __repr__(self):
        return "{cls}(sources=<{sources}>)".format(cls=__class__.__name__,
                                                   sources=", ".join(i for i in self._sources.keys()))

    def search(self, query, source: Type[MusicBase] = None) -> Dict[str, SearchResult]:
        sources_search = dict()
        if source:
            if source.__site_name__ not in self._sources:
                raise SourceNotRegisteredException("\"" + source.__site_name__ + "\" is not a registered source.")
            try:
                sources_search[source.__site_name__] = source(self._config[source.__site_name__]).search(query)
            except AvalandException:
                sources_search[source.__site_name__] = SearchResult(None, None, None)
                print(traceback.format_exc())
        else:
            for i in self._sources.keys():
                try:
                    sources_search[i] = self._sources[i](self._config[self._sources[i].__site_name__]).search(query)
                except AvalandException:
                    sources_search[i] = SearchResult(None, None, None)
                    print(traceback.format_exc())
        return sources_search
