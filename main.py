from PyQt5.QtWidgets import QApplication
import sys
from app import MainWindow
from PyQt5.QtGui import QFont, QFontDatabase
from utilities.fontManager import FontManager


# application initialization
app = QApplication(sys.argv)
FontManager.load_fonts()
main_window = MainWindow()
main_window.show()
sys.exit(app.exec_())