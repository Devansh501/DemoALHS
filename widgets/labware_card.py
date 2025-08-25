from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from widgets.button import ThemedButton

class LabwareCard(QWidget):
    def __init__(self, parentObj, data):
        super().__init__()

        # Give the root an id so we can target only it
        self.setObjectName("labwareCard")

        # Optional: ensure styled background is painted on plain QWidget
        self.setAttribute(Qt.WA_StyledBackground, True)

        # self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.setFixedSize(220, 150)

        shadow = QGraphicsDropShadowEffect(blurRadius=15, xOffset=3, yOffset=3, color=QColor(0,0,0,60))
        self.setGraphicsEffect(shadow)

        self.setStyleSheet("""
            QWidget#labwareCard {
                background: #E4EDFF;
                border-radius: 12px;
            }
            /* Children should not paint their own backgrounds */
            QWidget#labwareCard QLabel {
                background: transparent;
                color: #000;
            }
            QWidget#labwareCard QPushButton {
                background: #3A6EA5;
                color: white;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 12px;
            }
            QWidget#labwareCard QPushButton:hover {
                background: #2C5A8A;
            }
        """)

        # ----- layout/content -----
        main = QVBoxLayout(self)
        # main.setContentsMargins(6, 20, 6, 20)
        # main.setSpacing(6)

        name = QLabel(data["name"])
        f = QFont("Arial", 12); f.setBold(True)
        name.setFont(f)
        main.addWidget(name)

        # two detail lines
        detailWrapWidget = QWidget()
        detailWrapWidgetLayout = QVBoxLayout(detailWrapWidget)
        for d in (data.get("details") or [])[:2]:
            lbl = QLabel(f'{d.get("label", "")} : {d.get("value", "")}')
            detailWrapWidgetLayout.addWidget(lbl)

        main.addWidget(detailWrapWidget)
        # buttons row at bottom
        row = QHBoxLayout()
        row.setSpacing(10)
        info = ThemedButton("Info", "small")
        add  = ThemedButton("Add", "small")
        add.clicked.connect(parentObj.test)
        row.addWidget(info)
        row.addWidget(add)
        # main.addStretch(1)
        main.addLayout(row)
