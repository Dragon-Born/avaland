class SearchResult(object):

    def __init__(self, musics=None, albums=None, artists=None):
        self.musics = tuple(musics) if musics else tuple()
        self.albums = tuple(albums) if albums else tuple()
        self.artists = tuple(artists) if artists else tuple()
        self.record_count = len(self.musics) + len(self.albums) + len(self.artists)

    def to_dict(self):
        return {
            "musics": [{j: i.__dict__[j] if j != "source" else i.__dict__[j].__site_name__ for j in i.__dict__} for i in
                       self.musics],
            "albums": [{j: i.__dict__[j] if j != "source" else i.__dict__[j].__site_name__ for j in i.__dict__} for i in
                       self.albums],
            "artists": [{j: i.__dict__[j] if j != "source" else i.__dict__[j].__site_name__ for j in i.__dict__} for i
                        in self.artists],
        }

    def __repr__(self):
        musics = self.musics[0].full_title + ',...' if len(self.musics) > 0 else None
        albums = self.albums[0].full_title + ',...' if len(self.albums) > 0 else None
        artists = self.artists[0].full_name + ',...' if len(self.artists) > 0 else None
        return "{cls}(musics=<{musics}>, artists=<{artists}>, albums=<{albums}>)".format(cls=SearchResult.__name__,
                                                                                         musics=musics,
                                                                                         artists=artists,
                                                                                         albums=albums)
