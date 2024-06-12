import sys
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QGridLayout, QMenu, QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout
from PySide6.QtGui import QIcon, QAction

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Window properties
        self.setWindowTitle("Sprite Sheet Creator")

        #Class vars/data
        self.menu_items = {"File": ["New Sheet", "Open Sheet", "Save Sheet"], "Code": ["View Meta Code"]}
        self.sprite_size = (4, 4)
        self.grid_size = (8, 8)

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
    def __init__(self, grid_size:tuple, item_size:tuple):
        super().__init__()
        #Widget properties
        self.setAcceptDrops(True)

        #Class vars/data
        self.grid_x, self.grid_y = grid_size
        self.item_x, self.item_y = item_size
        self.accepted_files = ["jpg", "png"]

        self.contained_items = {} #Dict, each sprite with own part; {"file_path": {"name": "cool sprite"}}
        self.grid = []

        #GUI layouts
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)

        vspacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        hspacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.main_layout.addItem(vspacer, 4, 0, 1, -1)
        self.main_layout.addItem(hspacer, 3, 3, -1, 1)

        self.main_layout.setSpacing(0)

        self.draw_empty_grid()

    def draw_empty_grid(self):
        for row in range(self.grid_y):
            self.grid.append([])
            for column in range(self.grid_x):
                self.grid[-1].append(QPushButton("", self))
                self.main_layout.addWidget(self.grid[-1][-1], row*15, column*15, self.grid_y, self.grid_x)

        for row in self.grid:
            for button in row:
                button.setFixedSize(self.item_x*15, self.item_y*15)
    def dragEnterEvent(self, file): #Runs when any file/link dropped onto WIDGET not window, it's widget specific
        if file.mimeData().hasUrls(): #Only accepts dropped things that have a/multiple URL(s)
            file.accept()
        else:
            file.ignore()

    def dropEvent(self, file): #Runs when a file is actually dropped
        for i in file.mimeData().urls():
            split_path = str(i.toEncoded(), "utf-8").split("/") #Converting parsed URL to string that can be manipulated
            path = ""
            for i in split_path:
                if i == "" or i == "file:":
                    continue
                else:
                    i = i.replace("%20", " ")
                    if path == "": path += f"{i}"
                    else: path += f"/{i}"
            file_type = path.split(".")[-1]
            file_name = path.split(".")[0].split("/")[-1]
            if file_type in self.accepted_files: #If it is a file type we allow, add it to store of contained items
                drop_pos = file.position().toPoint()
                self.contained_items[f"{file_name}-{path}"] = {"path": path,
                                              "name": file_name,
                                              "type": file_type,
                                              "location": drop_pos}
                self.place_on_grid(self.contained_items[f"{file_name}-{path}"])

    def place_on_grid(self, item):
        button_at_pos = self.childAt(item["location"])
        button_at_pos.setIcon(QIcon(item["path"]))
        button_at_pos.setIconSize(QSize(self.item_x*15, self.item_y*15))
        button_at_pos.update()

    def update_grid_size(self, new_grid_size:tuple):
        self.grid_x, self.grid_y = new_grid_size

    def update_item_size(self, new_item_size:tuple):
        self.item_x, self.item_y = new_item_size

    def get_grid_size(self):
        return self.grid_x, self.grid_y

    def get_item_size(self):
        return self.item_x, self.item_y

    def get_contained_items(self):
        return self.contained_items

app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()