from PyQt5.QtWidgets import  QWidget, QLabel, QVBoxLayout, QGridLayout, QHBoxLayout
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import QFont
from widgets.icon_button import IconButton
from widgets.heading import Heading
from widgets.menu_button import MenuButton
from widgets.warning_dialog import WarningDialog
import sys

class HomeScreen(QWidget):
    def __init__(self,parentObj):
        super().__init__()

        # Container to hold both screens
        self.container = QWidget(self)

        # Screens
        self.screen1 = self.create_screen("Screen 1", "#2196F3")
        self.screen2 = self.create_screen("Screen 2", "#4CAF50")
       

        # Add screens to container
        self.screen1.setParent(self.container)
        self.screen2.setParent(self.container)


        # Screen1

        # Layout Setup
        screen1LayoutWrapper = QVBoxLayout(self.screen1)
        screen1Heading = Heading("   Menu", level=1)

        screen1MainWidget = QWidget()
        screen1GridLayout = QGridLayout(screen1MainWidget)

        pipetteButton = MenuButton("Pipette")
        labwareButton = MenuButton("Labware")
        quickLoadButton = MenuButton("Quick Load")
        newProtocolButton = MenuButton("New")

        screen1GridLayout.addWidget(pipetteButton, 0, 0)
        screen1GridLayout.addWidget(labwareButton, 0, 1)
        screen1GridLayout.addWidget(quickLoadButton, 1, 0)
        screen1GridLayout.addWidget(newProtocolButton, 1, 1)

        screen1GridLayout.setSpacing(40)
        screen1MainCover = QWidget()
        screen1MainElementWrapper = QHBoxLayout(screen1MainCover)
        screen1MainElementWrapper.addStretch()
        screen1MainElementWrapper.addWidget(screen1MainWidget)
        screen1MainElementWrapper.addStretch()

        

        screen1LayoutWrapper.addWidget(screen1Heading)
        screen1LayoutWrapper.addStretch()
        screen1LayoutWrapper.addWidget(screen1MainCover)
        screen1LayoutWrapper.addStretch()
        # Layout Setup End

        # Functionality

        pipetteButton.clicked.connect(lambda: parentObj.router("pipette_config"))
        labwareButton.clicked.connect(lambda: parentObj.router("labware"))
        newProtocolButton.clicked.connect(lambda: self.newProtocolHandle(parentObj))
        

        # Funtionality End



        # Screen2
        screen2LayoutWrapper = QVBoxLayout(self.screen2)
        screen2Heading = Heading("   Menu", level=1)

        screen2MainWidget = QWidget()
        screen2GridLayout = QGridLayout(screen2MainWidget)

        calibrationButton = MenuButton("Calibration",fontSize=17)
        simulationButton = MenuButton("Simulation",fontSize=18)
        settingsButton = MenuButton("Settings")
        comingSoonButton = MenuButton("Coming Soon ...")

        screen2GridLayout.addWidget(calibrationButton, 0, 0)
        screen2GridLayout.addWidget(simulationButton, 0, 1)
        screen2GridLayout.addWidget(settingsButton, 1, 0)
        screen2GridLayout.addWidget(comingSoonButton, 1, 1)

        screen2GridLayout.setSpacing(40)
        screen2MainCover = QWidget()
        screen2MainElementWrapper = QHBoxLayout(screen2MainCover)
        screen2MainElementWrapper.addStretch()
        screen2MainElementWrapper.addWidget(screen2MainWidget)
        screen2MainElementWrapper.addStretch()

        

        screen2LayoutWrapper.addWidget(screen2Heading)
        screen2LayoutWrapper.addStretch()
        screen2LayoutWrapper.addWidget(screen2MainCover)
        screen2LayoutWrapper.addStretch()
        
        # Functionality
        calibrationButton.clicked.connect(lambda: parentObj.router("calibration"))

        # # Buttons
        self.button1 = IconButton(
            icon_path=":/icons/rightArrow.png",
            size="large",
            primary_color="#ffffff",
            hover_color="#c1dff7",
            pressed_color="#C6CDD3",
            parent=self.screen1
        )
        self.button1.clicked.connect(self.slide_next)


        self.button2 = IconButton(
            icon_path=":/icons/leftArrow.png",
            size="large",
            primary_color="#ffffff",
            hover_color="#c1dff7",
            pressed_color="#C6CDD3",
            parent=self.screen2
        )
        self.button2.clicked.connect(self.slide_back)

        # Keep animations alive
        self.anim1 = None
        self.anim2 = None

    def create_screen(self, label, color):
        screen = QWidget()
        screen.setStyleSheet(f"background-color: transparent;")
        return screen

    def resizeEvent(self, event):
        """Update layout and positions when window resizes."""
        w, h = self.width(), self.height()

        # Resize the container to fill this widget
        self.container.setGeometry(0, 0, w, h)

        # Position screens
        self.screen1.setGeometry(0, 0, w, h)
        self.screen2.setGeometry(w, 0, w, h)  # Off-screen to the right

        # Position button1 at mid-right (on screen1)
        self.button1.move(
            w - self.button1.width() - 20,         # 20px from right edge
            (h - self.button1.height()) // 2       # vertical center
        )

        # Position button2 at mid-left (on screen2)
        self.button2.move(
            20,                                     # 20px from left edge
            (h - self.button2.height()) // 2       # vertical center
        )

        super().resizeEvent(event)


    def slide_next(self):
        w, h = self.width(), self.height()

        anim1 = QPropertyAnimation(self.screen1, b"geometry")
        anim1.setDuration(400)
        anim1.setEasingCurve(QEasingCurve.InOutQuad)
        anim1.setStartValue(QRect(0, 0, w, h))
        anim1.setEndValue(QRect(-w, 0, w, h))

        anim2 = QPropertyAnimation(self.screen2, b"geometry")
        anim2.setDuration(400)
        anim2.setEasingCurve(QEasingCurve.InOutQuad)
        anim2.setStartValue(QRect(w, 0, w, h))
        anim2.setEndValue(QRect(0, 0, w, h))

        anim1.start()
        anim2.start()
        self.anim1 = anim1
        self.anim2 = anim2

    def slide_back(self):
        w, h = self.width(), self.height()

        anim1 = QPropertyAnimation(self.screen2, b"geometry")
        anim1.setDuration(400)
        anim1.setEasingCurve(QEasingCurve.InOutQuad)
        anim1.setStartValue(QRect(0, 0, w, h))
        anim1.setEndValue(QRect(w, 0, w, h))

        anim2 = QPropertyAnimation(self.screen1, b"geometry")
        anim2.setDuration(400)
        anim2.setEasingCurve(QEasingCurve.InOutQuad)
        anim2.setStartValue(QRect(-w, 0, w, h))
        anim2.setEndValue(QRect(0, 0, w, h))

        anim1.start()
        anim2.start()
        self.anim1 = anim1
        self.anim2 = anim2
    
    def newProtocolHandle(self,parentObj):
        if(getattr(parentObj,"pipette_screen", None) is None and getattr(parentObj,"labware_screen", None) is None):
            dialog = WarningDialog(
            "Pipette and Labwares Configuration are missing!!",
            icon_path=":icons/warning.png",
            parent=self)
            result = dialog.exec_()
        elif(getattr(parentObj,"pipette_screen", None) is None):
            dialog = WarningDialog(
            "Pipette Configuration is missing!!",
            icon_path=":icons/warning.png",
            parent=self)
            result = dialog.exec_()
        elif(getattr(parentObj,"labware_screen", None) is None):
            dialog = WarningDialog(
            "Labware Configuration is missing!!",
            icon_path=":icons/warning.png",
            parent=self)
            result = dialog.exec_()
        else:
            parentObj.router("deck_arrng")
