from pony.orm import *

db = Database()


class DatabaseController:

    def __init__(self):
        self.db = db
        self.db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
        self.db.generate_mapping(check_tables=True, create_tables=True)


class Webradio(db.Entity):
    _table_ = 'Webradios'
    name = PrimaryKey(str, 400, column='name')
    genres = Set('Genre',  column='genres')
    url = Required(str, 500, column='url')
    icon = Optional(bytes, column='icon', lazy=True)
    country = Optional(str, 50, column='country')
    state = Optional(str, 50)
    language = Optional(str, 50, column='language')
    id = Optional(str)
    popularity = Optional(int, column="popularity")

    @property
    def has_genres(self):
        return not self.genres.is_empty()

class Genre(db.Entity):
    _table_ = 'Genres'
    name = PrimaryKey(str, 100, column='name', auto=True)
    webradios = Set(Webradio, column='webradios')

