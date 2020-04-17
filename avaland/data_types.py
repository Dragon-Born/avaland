from typing import Set, Tuple


class Music:
    id: int
    title: str
    artist: str
    full_title: str
    album: str
    image: str
    url: str

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
    id: int
    title: str
    artist: str
    full_title: str
    musics: Tuple[Music]
    image: str

    source = None

    def __init__(self, **kwargs):
        for i in kwargs.keys():
            setattr(self, i, kwargs[i].strip() if kwargs[i] and isinstance(kwargs[i], str) else kwargs[i])
        self.full_title = self.title + ' - ' + self.artist if self.artist else self.title

    def __repr__(self):
        return "<{id}: {album}>".format(id=str(self.id),
                                        album=self.title + " - " + self.artist if self.artist else self.title)


class Artist:
    id: int
    full_name: str
    musics: Tuple[Music]
    albums: Tuple[Album]
    image: str
    url: str

    source = None

    def __init__(self, **kwargs):
        for i in kwargs.keys():
            setattr(self, i, kwargs[i].strip() if kwargs[i] and isinstance(kwargs[i], str) else kwargs[i])

    def __repr__(self):
        return "<{id}: {name}>".format(id=str(self.id), name=self.full_name)
