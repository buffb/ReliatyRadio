from pony.orm import *

db = Database()


class DatabaseController:
    __instance = None

    @staticmethod
    def get_instance():
        if not DatabaseController.__instance:
            DatabaseController.__instance = DatabaseController()
        return DatabaseController.__instance

    def __init__(self):
        self.db = db
        self.db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
        self.db.generate_mapping(check_tables=True, create_tables=True)
        #self.populate_database()

    def get_radio_stations(self):
        yield Webradio.select()

    def get_radio_stations_by_popularity(self):
        return Webradio.select().order_by(desc(Webradio.popularity))

    def get_radio_stations_by_genre(self, genre):
        entity = Genre.get(name=genre)
        return Webradio.select(lambda r: entity in r.genres)

    def get_radio_stations_by_name(self, name):
        return Webradio.select(lambda r: name.lower() in r.name.lower())

    def get_genres_by_count(self, amount=0):
        genres = Genre.select(lambda g: count(g.name))
        if amount == 0:
            return genres[:]
        return genres[:amount:]

    @db_session
    def populate_database(self):
        rock = Genre(name="Rock")
        pop = Genre(name="Pop")
        klarinette = Genre(name="Wilde Klarinette")

        sender = "http://stream.landeswelle.de/lwt/mp3-192/web/stream.mp3"

        Webradio(name="69.666 FM Wilder Klarinettenrock", genres=[rock, klarinette], popularity=69, url=sender)
        Webradio(name="96.4 Pop ohne Korn", genres=[pop], popularity=96, url=sender)
        Webradio(name="33.3 Rockzipfel 2", genres=[rock], popularity=33, url=sender)
        Webradio(name="69.666 FM Pop and Stars", genres=[pop], popularity=69, url=sender)
        Webradio(name="Yopop", genres=[pop], popularity=911, url=sender)


class Webradio(db.Entity):
    _table_ = 'Webradios'
    name = PrimaryKey(str, 400, column='name')
    genres = Set('Genre', column='genres')
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
    id = PrimaryKey(int, auto=True)
    name = Required(str, 100, column='name', auto=True)
    webradios = Set(Webradio, column='webradios')


if __name__ == '__main__':
    d = DatabaseController()
    with db_session:
        all = d.get_radio_stations()
        genre_rock = d.get_radio_stations_by_genre("Rock")[:]
        genre_pop = d.get_radio_stations_by_genre("Pop")[:]
        genre_klarinette = d.get_radio_stations_by_genre("Klarinette")[:]
        station_name = d.get_radio_stations_by_name("zipfel")[:]
        popularity = d.get_radio_stations_by_popularity()[:]
        genres = d.get_genres_by_count()
        yolo = ""
