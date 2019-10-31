import threading
from io import BytesIO
from PIL import Image

import requests
from requests import Timeout

from DatabaseController import DatabaseController, Webradio, db_session, Genre


class CrawlerController():
    def __init__(self):
        self.dbc = DatabaseController()
        self.crawlers = []


class Crawler(object):
    def __init__(self):
        self.address = "localhost"
        self.results = {}

    def crawl(self):
        pass


class RadiodeCrawler(Crawler):
    def __init__(self):
        super().__init__()
        self.address = ""
        # self.api = "ia9p4XYXmOPEtXzL"


class RadioBrowserCrawler(Crawler):
    lock = threading.RLock()

    def __init__(self, cc):
        super().__init__()
        self.cc = cc
        self.amount = 0
        self.current = 0

        self.address = 'http://www.radio-browser.info/webservice/json/stations/bycountryexact/Germany'

    @db_session
    def crawl(self):
        resp = requests.get(url=self.address)
        data = resp.json()
        self.amount = len(data)
        for station in data:
            self.process_station(station)

    def process_station(self, station):
        self.current += 1
        print(str(self.current) + "/" + str(self.amount))

        name = station["name"]
        url = station["url"]

        tags = station["tags"].split(",")
        genres = []
        for genre in tags:
            if genre is None or genre == "" or len(genre) > 100: continue
            if not Genre.get(name=genre):
                genres.append(Genre(name=genre))
            else:
                genres.append(Genre.get(name=genre))

        iconurl = station["favicon"]
        icon = None
        if iconurl is not None:
            try:
                response = requests.get(iconurl, timeout=(10, 10))
                if not response:
                    return
                icon = BytesIO(response.content).getvalue()
            except Timeout:
                print("Timeout")
                return
            except:
                print("Error")
                return

        popularity = int(station["votes"]) + int(station["clickcount"])

        if Webradio.get(name=name) is not None:
            return

        if icon and name and url and popularity:
            Webradio(name=name, genres=genres, url=url, icon=icon, popularity=popularity)
            self.cc.dbc.db.commit()


if __name__ == '__main__':
    c = CrawlerController()
    c.crawlers.append(RadioBrowserCrawler(c))

    for cr in c.crawlers:
        cr.crawl()
