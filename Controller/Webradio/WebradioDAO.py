from pony.orm import desc

from Model.Webradio import Webradio


class WebradioDAO:
    def __init__(self, db):
        self.db = db

    def get_radio_stations(self):
        return Webradio.select()

    def get_radio_stations_by_popularity(self):
        return Webradio.select().order_by(desc(Webradio.popularity))

    def get_radio_stations_by_genre(self, genre):
        return Webradio.select().w

    def get_radio_stations_by_name(self, name):
        pass
