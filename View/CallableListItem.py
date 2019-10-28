from PyQt5.QtWidgets import QListWidgetItem


class CallableListItem(QListWidgetItem):
    def __init__(self,name="", parent=None, item=None, params=None):
        super().__init__(name,parent)
        self.item = item
        self.params = params
