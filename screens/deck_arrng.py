from PyQt5.QtWidgets import QWidget,QHBoxLayout,QVBoxLayout,QApplication
from PyQt5.QtCore import Qt
from widgets.button import ThemedButton
from widgets.heading import Heading

class DeckArrangement(QWidget):
    def __init__(self, parentObj):
        super().__init__()
        screenDimensions = QApplication.primaryScreen().size()
        screenWrapper = QVBoxLayout(self)
        
        # Heading
        screenWrapper.addWidget(Heading("Deck Arrangement",level = 1))
        
        # main Area
        mainWidget = QWidget()
        mainWidget.setStyleSheet("background-color: #ffffff;border-radius:12px;")
        mainWidget.setFixedSize(int(screenDimensions.width() * 0.90), int(screenDimensions.height() * 0.7))
        screenWrapper.addWidget(mainWidget,alignment=Qt.AlignCenter)
        # bottom Navigation
        navLayout = QHBoxLayout()
        backButton = ThemedButton("Back")
        nextButton = ThemedButton("Next")
        navLayout.addWidget(backButton)
        navLayout.addStretch(1)
        navLayout.addWidget(nextButton)
        navLayout.setContentsMargins(20, 20, 20, 20)
        
        backButton.clicked.connect(lambda: parentObj.router('home'))
        nextButton.clicked.connect(lambda: parentObj.router('pipette_selectn'))
        
        screenWrapper.addLayout(navLayout)
        
    
    