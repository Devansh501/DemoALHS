from PyQt5.QtWidgets import QApplication
import sys
from app import MainWindow
from PyQt5.QtGui import QFont, QFontDatabase
from utilities.fontManager import FontManager
from utilities.utils import Utils


# application initialization
app = QApplication(sys.argv)
FontManager.load_fonts()
main_window = MainWindow()
ss = Utils.load_stylesheet("globals.qss")
main_window.setStyleSheet(ss)
main_window.show()
sys.exit(app.exec_())