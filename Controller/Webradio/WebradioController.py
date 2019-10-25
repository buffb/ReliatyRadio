from DatabaseController import DatabaseController
from Controller.Webradio.WebradioDAO import WebradioDAO


class WebradioController(DatabaseController):
    def __init__(self):
        self.dao = WebradioDAO(self.db)
        super().__init__()
        self.webradio = None
        self.playing = ""
        self.player = None
