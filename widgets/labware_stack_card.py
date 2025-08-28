from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel,QPushButton
from PyQt5.QtGui import QFont, QColor, QIcon
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from widgets.button import ThemedButton

class LabwareStackCard(QWidget):
    def __init__(self, parentObj, data):
        super().__init__()
        # Object name for styling
        self.setObjectName("labwareStackCard")
        self.setAttribute(Qt.WA_StyledBackground, True)

        # Fixed size (adjust as needed)
        self.setFixedSize(220, 55)

        # Drop shadow
        shadow = QGraphicsDropShadowEffect(blurRadius=15, xOffset=3, yOffset=3, color=QColor(0, 0, 0, 60))
        self.setGraphicsEffect(shadow)

        # Style
        self.setStyleSheet("""
            QWidget#labwareStackCard {
                background: #E4EDFF;
                border-radius: 6px;
            }
            QWidget#labwareStackCard QLabel {
                background: transparent;
                color: #000;
            }
            QWidget#labwareStackCard QPushButton {
                background: #3A6EA5;
                color: white;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 12px;
            }
            QWidget#labwareStackCard QPushButton:hover {
                background: #2C5A8A;
            }
        """)

        # Main vertical layout
        mainLayout = QHBoxLayout(self)
        mainLayout.setContentsMargins(12, 12, 12, 12)
        mainLayout.setSpacing(10)
        
        leftLayout = QVBoxLayout()

        # ---- Title ----
        name = QLabel(f'{data["name"]}')
        font = QFont("Arial", 8)
        font.setBold(True)
        name.setFont(font)
        leftLayout.addWidget(name)
        # mainLayout.addWidget(name)

        # ---- First detail (subtitle) ----
        subtitle = QLabel(data.get("details", [{}])[0].get("value", ""))
        subtitleFont = QFont("Arial", 7)
        subtitle.setFont(subtitleFont)
        leftLayout.addWidget(subtitle)
        # mainLayout.addWidget(subtitle)

        # ---- Buttons row ----
        btnLayout = QHBoxLayout()
        btnLayout.addStretch()  # Push buttons to the right
        infoBtn = QPushButton()
        dltBtn = QPushButton()

        # Set icons (replace with your icon paths)
        infoBtn.setIcon(QIcon(":icons/info.png"))
        dltBtn.setIcon(QIcon(":icons/delete.png"))

        # Optional: Set button size (to make it square)
        infoBtn.setFixedSize(32, 32)
        dltBtn.setFixedSize(32, 32)

        # Remove borders and background (make them clean)
        infoBtn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border-radius: 32px;
            }
            QPushButton:hover {
                background: #f0f0f0;
            }
        """)
        dltBtn.setStyleSheet("""
            QPushButton {
                background:transparent;
                border-radius: 32px;
            }
            QPushButton:hover {
                background: #f0f0f0;
            }
        """)

        btnLayout.addWidget(infoBtn)
        btnLayout.addWidget(dltBtn)
        btnLayout.setSpacing(0)
        
        infoBtn.clicked.connect(lambda x: parentObj.setInfo(data["index"]))
        dltBtn.clicked.connect(lambda x: parentObj.removeAddedLabwares(data["index"]))

        # Add button layout at bottom
        # mainLayout.addStretch()  # Push everything else up
        mainLayout.addLayout(leftLayout)
        mainLayout.addLayout(btnLayout)
