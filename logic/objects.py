class WebPag:
    def __init__(self):
        self.api_search_request = ""
        self.html_content = ""
        self.html_url = ""
        self.extracted_playlist_node = ""
        self.extracted_wiki_node = ""
        self.extracted_playlist_text = ""
        self.extracted_wiki_text = ""


class AlbumObject:
    def __init__(self):
        self._complete_file_path = ""
        self._clean_file_name = ""
        self._file_name = ""
        self._artist_name = ""
        self._title_name = ""
        self._file_ending = ""
        self._release_year = ""
        self._genre = ""

        # self._complete_file_path: string
        # self._clean_file_path: string
        # self._file_name: string
        # self._artist_name: string
        # self._title_name: string
        # self._file_ending: string
        # self._release_year: string

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        self._file_name = value

    @property
    def artist_name(self):
        return self._artist_name

    @artist_name.setter
    def artist_name(self, value):
        self._artist_name = value

    @property
    def release_year(self):
        return self._release_year

    @release_year.setter
    def release_year(self, value):
        self._release_year = value

    @property
    def title_name(self):
        return self._title_name

    @title_name.setter
    def title_name(self, value):
        self._title_name = value

    @property
    def file_ending(self):
        return self._file_ending

    @file_ending.setter
    def file_ending(self, value):
        self._file_ending = value

    @property
    def complete_file_path(self):
        return self._complete_file_path

    @complete_file_path.setter
    def complete_file_path(self, value):
        self._complete_file_path = value

    @property
    def clean_file_path(self):
        return self._clean_file_name

    @clean_file_path.setter
    def clean_file_path(self, value):
        self._clean_file_name = value

    @property
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, value):
        self._genre = value
