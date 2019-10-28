from io import BytesIO
from multiprocessing import Manager
from pathos.pools import ProcessPool as Pool

import requests

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
    def __init__(self):
        super().__init__()
        self.amount = None
        self.address = 'http://www.radio-browser.info/webservice/json/stations/bycountryexact/Germany'

    @db_session
    def crawl(self):
        resp = requests.get(url=self.address)
        data = resp.json()
        self.amount = len(data)
        m = Manager()
        self.lock = m.RLock()
        self.counter = m.Value(int, 0)
        with Pool(1) as p:
            p.map(self.process_station, data)

    def process_station(self, station):

        self.lock.acquire(True)
        self.counter.set(self.counter.get() + 1)
        print(str(self.counter.get()) + "/" + str(self.amount))
        self.lock.release()

        name = station["name"]
        url = station["url"]

        tags = station["tags"].split(",")
        genres = []
        for genre in tags:
            if genre == "" or len(genre) > 100: continue
            if not Genre.get(name=genre):
                self.lock.acquire(True)
                genres.append(Genre(name=genre))
                self.lock.release()
            else:
                genres.append(Genre.get(name=genre))

        iconurl = station["favicon"]
        icon = None
        if iconurl is not None:
            try:
                icon = BytesIO(requests.get(iconurl, stream=True).raw)
            except:
                return

        popularity = int(station["votes"]) + int(station["clickcount"])

        if icon and name and url and popularity:
            self.lock.acquire(True)
            Webradio(name=name, genres=genres, url=url, icon=icon, country="Deutschland")
            self.lock.release()


if __name__ == '__main__':
    c = CrawlerController()
    c.crawlers.append(RadioBrowserCrawler())

    for cr in c.crawlers:
        cr.crawl()
