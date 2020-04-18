class SearchResult:

    def __init__(self, musics, albums, artists):
        self.musics = tuple(musics)
        self.albums = tuple(albums)
        self.artists = tuple(artists)
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
