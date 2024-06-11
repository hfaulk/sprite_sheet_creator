import sys
from PySide6.QtCore import QSize, Qt, QFile, QStringListModel
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout, QLineEdit, QCompleter
from PySide6.QtGui import QIcon, QPixmap, QFont

class MainWindow(QMainWindow):
    def __init__(self):
        ...




app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()