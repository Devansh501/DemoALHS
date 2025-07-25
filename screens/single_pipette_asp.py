from PyQt5.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QSpacerItem, QSizePolicy
from PyQt5.QtGui import QGuiApplication
from widgets.button import ThemedButton
from widgets.heading import HeadingWidget
from widgets.awesome_grid import ButtonGridWidget

class SinglePipetteAsp(QWidget):
    def __init__(self, parentObj):
        super().__init__()
        self.setStyleSheet("""
    QWidget {
        background: qlineargradient(
            spread:pad,
            x1:0, y1:0,
            x2:1, y2:1,
            stop:0 #0f2a44,
            stop:1 #1a4d7a
        );
    }
""")
        self.screen_width = QGuiApplication.primaryScreen().geometry().width()
        self.screen_height = QGuiApplication.primaryScreen().geometry().height()

        self.setWindowTitle("Single Pipette Aspiration")
        layout = QVBoxLayout()
        heading = HeadingWidget("Single Pipette Aspiration", alignment='center', stretchable=True)
        
        # Left Area
        playarea = QWidget()
        playareaLayout = QHBoxLayout(playarea)
        playareaLayout.setContentsMargins(25, 0, 25, 0)

        
        SinglePipetteAspGrid = ButtonGridWidget(12, 12)
        gridWrapper = QWidget()

        gridWrapper.setMaximumWidth(int(self.screen_width * 0.50))
        gridWrapper.setMaximumHeight(int(self.screen_height * 0.60))
        gridWrapperLayout = QVBoxLayout(gridWrapper) 
        gridWrapperLayout.addWidget(SinglePipetteAspGrid)
        
        # Center Area
        aspirationOptionsWrapper = QWidget()
        aspirationOptionsWrapperLayout = QVBoxLayout(aspirationOptionsWrapper)
        aspirationOptionsWrapperLayout.setContentsMargins(0, 0, 0, 0)
        
        ASpirationData = ThemedButton("Aspiration Data", size="large", primary_color="#1a4d7a", hover_color="#246ca3", pressed_color="#153b60")

        playareaLayout.addWidget(gridWrapper)
        playareaLayout.addSpacerItem(QSpacerItem(1, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        playareaLayout.addWidget(aspirationOptionsWrapper)
        playareaLayout.addSpacerItem(QSpacerItem(1, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        playareaLayout.addWidget(ASpirationData)

        layout.addWidget(heading,1)
        layout.addWidget(playarea, 8)


        self.setLayout(layout) 