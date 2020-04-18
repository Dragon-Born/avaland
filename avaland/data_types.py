from typing import Tuple


class Music:
    id = None  # type: int
    title = None  # type: str
    artist = None  # type: str
    full_title = None  # type: str
    album = None  # type: str
    image = None  # type: str
    url = None  # type: str

    source = None

    def __init__(self, **kwargs):
        for i in kwargs.keys():
            setattr(self, i, kwargs[i].strip() if kwargs[i] and isinstance(kwargs[i], str) else kwargs[i])
        self.full_title = self.title + ' - ' + self.artist if self.artist else self.title

    def download(self, path=None):
        return self.source({}).download(self.id, path)

    def __getitem__(self, item):
        return None

    def __repr__(self):
        return "<{id}: {music}>".format(id=str(self.id),
                                        music=self.title + " - " + self.artist if self.artist else self.title)


class Album:
    id = None  # type: int
    titl = None  # type: str
    artis = None  # type: str
    full_title = None  # type: str
    musics = None  # type: Tuple[Music]
    image = None  # type: str

    source = None

    def __init__(self, **kwargs):
        for i in kwargs.keys():
            setattr(self, i, kwargs[i].strip() if kwargs[i] and isinstance(kwargs[i], str) else kwargs[i])
        self.full_title = self.title + ' - ' + self.artist if self.artist else self.title

    def __repr__(self):
        return "<{id}: {album}>".format(id=str(self.id),
                                        album=self.title + " - " + self.artist if self.artist else self.title)


class Artist:
    id = None  # type: int
    full_name = None  # type: str
    musics = None  # type: Tuple[Music]
    albums = None  # type: Tuple[Album]
    image = None  # type: str
    url = None  # type: str

    source = None

    def __init__(self, **kwargs):
        for i in kwargs.keys():
            setattr(self, i, kwargs[i].strip() if kwargs[i] and isinstance(kwargs[i], str) else kwargs[i])

    def __repr__(self):
        return "<{id}: {name}>".format(id=str(self.id), name=self.full_name)
