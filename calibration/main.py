from PyQt5.QtWidgets import QApplication
from calibration_screen import CalibrationScreen
import sys
# from Machine_Code.Machine_Backend_V2 import LHSFunction
if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = CalibrationScreen()
    screen.show()
    screen.showFullScreen()
    sys.exit(app.exec_())
