import time
import traceback
from typing import Type, Dict

from avaland.exceptions import AvalandException, SourceNotRegisteredException
from avaland.music_base import MusicBase
from avaland.search import SearchResult
import multiprocessing as mp


class SourceManager:
    _config = dict()
    _sources = dict()

    def __init__(self):
        pass

    def register(self, source, config=None):
        # type: (Type[MusicBase], dict) -> SourceManager
        if config is None:
            config = {}
        self._sources[source.__site_name__] = source
        self._config[source.__site_name__] = config
        return self

    def __repr__(self):
        return "{cls}(sources=<{sources}>)".format(cls=SourceManager.__name__,
                                                   sources=", ".join(i for i in self._sources.keys()))

    @staticmethod
    def _search(query, source, return_dict):
        try:
            return_dict[type(source).__name__] = source.search(query)
        except AvalandException:
            return_dict[type(source).__name__] = SearchResult(None, None, None)
            print(traceback.format_exc())

    def search(self, query, source=None):
        # type: (str, Type[MusicBase]) -> Dict[str, SearchResult]
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
            multi_manager = mp.Manager()
            sources_search = multi_manager.dict()
            jobs = []
            for i in self._sources.keys():
                source = self._sources[i](self._config[self._sources[i].__site_name__])
                p = mp.Process(target=self._search, args=(query, source, sources_search))
                jobs.append(p)
                p.start()
            for proc in jobs:
                proc.join()
        return sources_search
