from PyQt5.QtWidgets import QApplication
import sys
from app import MainWindow


# application initialization
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec_())