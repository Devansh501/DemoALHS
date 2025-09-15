from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QWidget
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QRect, QObject, pyqtSlot
from pathlib import Path
from resources import resources
from utilities.utils import Utils



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("Global")
        
        # The Parent Object
        self.parentObj = {}
        # Load QSS
        stylesheet = Utils.load_stylesheet("globals.qss")
        self.setStyleSheet(stylesheet)

        # self.showFullScreen()
        self.setFixedSize(1024, 600)

        # Use a QStackedWidget to hold and switch screens
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.current_screen = None

        # Animation placeholders (to keep them in scope)
        self.anim_in = None
        self.anim_out = None

        # Start with the home screen
        self.router("home", animate=False)

    def router(self, screen_name: str, animate=True):
        new_widget = self.load_screen(screen_name)
        self.stack.addWidget(new_widget)

        if not self.current_screen or not animate:
            # No animation, switch immediately
            self.stack.setCurrentWidget(new_widget)
            if self.current_screen:
                self.stack.removeWidget(self.current_screen)
                self.current_screen.deleteLater()
            self.current_screen = new_widget
            return

        # Prepare animation
        width = self.stack.width()
        height = self.stack.height()

        # Position the new widget to the right of current view
        new_widget.setGeometry(QRect(width, 0, width, height))

        # Animate new widget sliding in
        self.anim_in = QPropertyAnimation(new_widget, b"geometry")
        self.anim_in.setDuration(400)
        self.anim_in.setStartValue(QRect(width, 0, width, height))
        self.anim_in.setEndValue(QRect(0, 0, width, height))
        self.anim_in.setEasingCurve(QEasingCurve.InOutQuad)

        # Animate current screen sliding out to the left
        self.anim_out = QPropertyAnimation(self.current_screen, b"geometry")
        self.anim_out.setDuration(400)
        self.anim_out.setStartValue(QRect(0, 0, width, height))
        self.anim_out.setEndValue(QRect(-width, 0, width, height))
        self.anim_out.setEasingCurve(QEasingCurve.InOutQuad)

        # Cleanup after animation
        @pyqtSlot()
        def on_animation_finished():
            self.stack.setCurrentWidget(new_widget)
            self.stack.removeWidget(self.current_screen)
            self.current_screen.deleteLater()
            self.current_screen = new_widget

        self.anim_in.finished.connect(on_animation_finished)
        self.anim_out.start()
        self.anim_in.start()

    def load_screen(self, screen_name: str) -> QWidget:
        if screen_name == "home":
            from screens.home import HomeScreen
            return HomeScreen(self)
        elif screen_name == "pipette_config":
            from screens.pipette_config import PipetteConfigScreen
            return PipetteConfigScreen(self)
        elif screen_name == "labware":
            from screens.labware import LabwareScreen
            return LabwareScreen(self)
        elif screen_name == "deck_arrng":
            from screens.deck_arrng import DeckArrangement
            return DeckArrangement(self)
        elif screen_name == "pipette_selectn":
            from screens.pipette_selectn import PipetteSelection
            return PipetteSelection(self)
        elif screen_name == "reagent_config":
            from screens.reagent_config import ReagentConfiguration
            return ReagentConfiguration(self)
        elif screen_name == "calibration":
            from calibration.calibration_screen import CalibrationScreen
            return CalibrationScreen(self)
        else:
            raise ValueError(f"Unknown screen: {screen_name}")
