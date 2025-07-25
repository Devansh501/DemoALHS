from PyQt5.QtWidgets import QWidget,QHBoxLayout
from widgets.button import ThemedButton

class HomeScreen(QWidget):
    def __init__(self, parentObj):
        super().__init__()
        self.setWindowTitle("Home")
        layout = QHBoxLayout()
        single_pipette_button = ThemedButton("Single Pipette",size="large")
        multi_pipette_button = ThemedButton("Multi Pipette",size="large")

        single_pipette_button.clicked.connect(lambda: parentObj.router("single_pipette_asp"))
        multi_pipette_button.clicked.connect(lambda: parentObj.router("multi_pipette_asp"))
        
        layout.addWidget(single_pipette_button)
        layout.addWidget(multi_pipette_button)
        self.setLayout(layout)

