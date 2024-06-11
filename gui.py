import sys
from PySide6.QtCore import QSize, Qt, QFile, QStringListModel
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout, QLineEdit, QCompleter, QMenu
from PySide6.QtGui import QIcon, QPixmap, QFont, QAction

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Window properties
        self.setWindowTitle("Sprite Sheet Creator")
        self.setAcceptDrops(True)

        #Class vars/data
        self.menu_items = {"File": ["New Sheet", "Open Sheet", "Save Sheet"], "Code": ["View Meta Code"]}
        self.sprite_size = (4,4)
        self.grid_size = (32, 32)

        #Build GUI
        self._build_menu_bar()

        self.main_vertical = QVBoxLayout()
        self.main_vertical.addWidget(PreviewGrid(self.grid_size, self.sprite_size))

        widget = QWidget()
        widget.setLayout(self.main_vertical)
        self.setCentralWidget(widget)

    def _build_menu_bar(self):
        #Create bar
        bar = self.menuBar()
        self.setMenuBar(bar)

        self.bar_contents = {}

        #Populate bar
        for title in self.menu_items.keys():
            self.bar_contents[title] = {"Menu": QMenu(f"&{title}", self)} #Creates sub-dict for each menu item
            bar.addMenu(self.bar_contents[title]["Menu"])
            for subtitle in self.menu_items[title]: #Adds each sub item for each menu item
                action = QAction(self)
                action.setText(subtitle)
                self.bar_contents[title][subtitle] = action
                self.bar_contents[title]["Menu"].addAction(action)

class PreviewGrid(QWidget):
    def __init__(self, grid_size:tuple, sprite_size:tuple):
        super().__init__()
        #Widget properties
        self.setAcceptDrops(True)

        #Class vars/data
        self.grid_x, self.grid_y = grid_size
        self.item_x, self.item_y = sprite_size
        self.accepted_files = ["jpg", "png"]

        self.contained_items = {} #Dict, each sprite with own part; {"file_path": {"name": "cool sprite"}}

        #GUI layouts
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

    def draw_grid(self):
        pass

    def dragEnterEvent(self, file): #Runs when any file/link dropped onto WIDGET not window, it's widget specific
        if file.mimeData().hasUrls(): #Only accepts dropped things that have a/multiple URL(s)
            file.accept()
        else:
            file.ignore()

    def dropEvent(self, file): #Runs when a file is actually dropped
        for i in file.mimeData().urls():
            path = str(i.toEncoded(), "utf-8") #Converting parsed URL to string that can be manipulated
            file_type = path.split(".")[-1]
            file_name = path.split(".")[0].split("/")[-1]
            if file_type in self.accepted_files: #If it is a file type we allow, add it to store of contained items
                self.contained_items[path] = {"name": file_name, "type": file_type} #Could add more attributes later

app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()