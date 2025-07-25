from PyQt5.QtWidgets import QWidget,QHBoxLayout
from widgets.button import ThemedButton

class MultiPipetteAsp(QWidget):
    def __init__(self, parentObj):
        super().__init__()
        self.setWindowTitle("Single Pipette Aspiration")
        btn = ThemedButton("Multi-Aspiration", self)
        layout = QHBoxLayout()
        layout.addWidget(btn)
        self.setLayout(layout)